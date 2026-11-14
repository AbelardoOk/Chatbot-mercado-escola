#!/usr/bin/env python3
"""Gera frases de treinamento usando diretamente a API oficial da OpenAI.

Este script é independente de chatbot.llm e de scripts/gerar_dados_llm.py.
Execute a partir da raiz do repositório:

    python scripts/gerar_dados_gpt.py --testar-conexao
    python scripts/gerar_dados_gpt.py
    python scripts/gerar_dados_gpt.py --rotulos horario localizacao --n 8

A chave é lida do .env (open_api_key=...) ou do ambiente
(OPENAI_API_KEY / open_api_key). Nunca coloque a chave no código ou no Git.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
import unicodedata
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent

# CONFIGURAÇÃO: ajuste estes valores conforme a geração desejada.
MODELO = "gpt-5.5"
FRASES_POR_ESTILO = 10
ROTULOS_PADRAO = None  # None = todas as intenções + chitchat + fora_dominio
ESTILOS = [
    "perguntas completas e educadas",
    "mensagens curtas e informais, com abreviações naturais",
    "mensagens com erros leves de digitação, acentuação ou pontuação",
    "mensagens contextualizadas, como alguém explicando sua situação",
    "mensagens muito curtas, de 1 a 4 palavras",
]
MAX_TENTATIVAS_JSON = 3
MAX_COMPLETION_TOKENS = 1800
LIMIAR_SIMILARIDADE = 0.94
ARQUIVO_SAIDA = "dados/gerados_gpt.csv"
ARQUIVO_PROMPTS = "dados/prompts_gpt.md"
CHAVE_ENV = "open_api_key"  # também aceita OPENAI_API_KEY

COLUNAS = ["texto", "intencao", "origem"]


def ler_env(caminho: Path) -> dict[str, str]:
    """Lê pares simples CHAVE=valor de .env, sem depender de python-dotenv."""
    valores: dict[str, str] = {}
    if not caminho.exists():
        return valores
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#") or "=" not in linha:
            continue
        chave, _, valor = linha.partition("=")
        valores[chave.strip()] = valor.strip().strip('"').strip("'")
    return valores


def obter_chave(caminho_env: Path | None = None) -> str | None:
    """Obtém a chave do ambiente ou do .env; aceita o nome pedido pelo usuário."""
    for nome in (CHAVE_ENV, "OPENAI_API_KEY"):
        valor = os.environ.get(nome)
        if valor and valor.strip():
            return valor.strip()
    valores = ler_env(caminho_env or (RAIZ / ".env"))
    for nome in (CHAVE_ENV, "OPENAI_API_KEY"):
        valor = valores.get(nome)
        if valor and valor.strip() and "cole-aqui" not in valor.casefold():
            return valor.strip()
    return None


def criar_cliente(chave: str):
    """Cria o cliente oficial da OpenAI; não usa URL nem credenciais da OpenRouter."""
    try:
        from openai import OpenAI
    except ImportError as erro:  # pragma: no cover - depende do ambiente
        raise RuntimeError("Instale o SDK oficial: pip install openai") from erro
    return OpenAI(api_key=chave)


def normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFKC", texto).casefold()
    texto = re.sub(r"[^\w\s]", " ", texto, flags=re.UNICODE)
    return " ".join(texto.split())


def ler_frases_json(conteudo: str) -> list[str]:
    """Valida o objeto JSON e filtra frases com conteúdo utilizável."""
    objeto = json.loads(conteudo)
    if not isinstance(objeto, dict) or not isinstance(objeto.get("frases"), list):
        raise ValueError('A resposta JSON precisa conter uma lista chamada "frases".')
    frases = []
    for item in objeto["frases"]:
        if not isinstance(item, str):
            continue
        frase = " ".join(item.strip().split())
        if 3 <= len(frase) <= 300:
            frases.append(frase)
    if not frases:
        raise ValueError("A resposta JSON não contém frases válidas.")
    return frases


def descricao_rotulo(config, rotulo: str) -> str:
    if rotulo == "chitchat":
        return (
            "conversa social: cumprimentos, agradecimentos, despedidas, confirmações, "
            "elogios, risadas e perguntas sobre o próprio chatbot; sem pedidos de informação"
        )
    if rotulo == "fora_dominio":
        return (
            f"assuntos que o chatbot NÃO atende. Ele atende somente {config.tema} "
            f"({config.assuntos()}). Inclua assuntos cotidianos e temas universitários "
            "que não sejam dúvidas sobre o Mercado Escola."
        )
    return config.intencoes[rotulo].descricao


def montar_prompt(config, rotulo: str, quantidade: int, estilo: str) -> str:
    outras = [
        info.descricao for nome, info in config.intencoes.items() if nome != rotulo
    ]
    restricao = ""
    if rotulo not in {"chitchat", "fora_dominio"} and outras:
        restricao = "\nNão gere perguntas sobre estas outras intenções: " + "; ".join(outras) + "."

    return f"""Gere dados sintéticos para treinar um classificador de intenções de um chatbot brasileiro.

O chatbot atende exclusivamente dúvidas sobre: {config.tema}.
Rótulo que deve ser gerado: {rotulo}.
Significado do rótulo: {descricao_rotulo(config, rotulo)}.
Estilo desta rodada: {estilo}.
Quantidade exata: {quantidade} frases.

REGRAS:
- Escreva em português brasileiro natural, como mensagens reais de estudantes e visitantes.
- Varie estrutura, vocabulário, tamanho e forma de perguntar.
- Não gere apenas substituições de sinônimos nem frases quase idênticas.
- Cada frase deve pertencer inequivocamente ao rótulo solicitado.
- Para fora_dominio, inclua assuntos vizinhos à vida universitária e assuntos cotidianos.
- Não invente informações ou respostas sobre o Mercado Escola.
- Não inclua explicações, respostas, rótulos, numeração ou dados pessoais.
- Gere exatamente {quantidade} frases distintas.{restricao}

Retorne exclusivamente um objeto JSON válido no formato {{"frases": ["mensagem 1", "mensagem 2"]}}.
Não inclua Markdown nem texto fora do JSON."""


def solicitar_json(cliente, prompt: str, modelo: str = MODELO) -> str:
    """Faz uma chamada real ao endpoint Chat Completions da OpenAI."""
    resposta = cliente.chat.completions.create(
        model=modelo,
        messages=[
            {"role": "system", "content": "Você gera dados de treinamento. Responda somente JSON válido."},
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
        max_completion_tokens=MAX_COMPLETION_TOKENS,
    )
    conteudo = resposta.choices[0].message.content
    if not conteudo:
        raise ValueError("A API retornou conteúdo vazio.")
    return conteudo


def testar_conexao(cliente, modelo: str = MODELO) -> str:
    """Executa uma chamada curta e valida que chave, modelo e endpoint funcionam."""
    conteudo = solicitar_json(
        cliente,
        'Responda exatamente com JSON contendo status="ok" e uma mensagem curta de confirmação.',
        modelo=modelo,
    )
    objeto = json.loads(conteudo)
    if objeto.get("status") != "ok":
        raise RuntimeError(f"A API respondeu, mas o teste não retornou status=ok: {objeto!r}")
    return str(objeto.get("mensagem", "Conexão autenticada e resposta JSON recebida."))


def gerar_lote(cliente, config, rotulo: str, estilo: str, quantidade: int,
               modelo: str = MODELO, tentativas: int = MAX_TENTATIVAS_JSON) -> tuple[list[str], str, int]:
    prompt = montar_prompt(config, rotulo, quantidade, estilo)
    ultimo_erro = None
    for tentativa in range(1, tentativas + 1):
        try:
            frases = ler_frases_json(solicitar_json(cliente, prompt, modelo=modelo))
            if len(frases) < quantidade:
                raise ValueError(f"Recebidas {len(frases)} frases; esperadas {quantidade}.")
            return frases[:quantidade], prompt, tentativa
        except (json.JSONDecodeError, ValueError) as erro:
            ultimo_erro = erro
    raise RuntimeError(
        f"Não foi possível gerar {quantidade} frases válidas para {rotulo}/{estilo} "
        f"após {tentativas} tentativas: {ultimo_erro}"
    )


def deduplicar(novos: list[dict], existentes: list[dict], limiar: float = LIMIAR_SIMILARIDADE):
    """Filtra novos dados contra os existentes e entre si, sem reescrever linhas antigas."""
    aceitos: list[dict] = []
    por_rotulo: dict[str, list[str]] = {}
    rotulos_exatos: dict[str, str] = {}
    for item in existentes:
        chave = normalizar(str(item.get("texto", "")))
        if chave:
            rotulos_exatos.setdefault(chave, str(item.get("intencao", "")))
            por_rotulo.setdefault(str(item.get("intencao", "")), []).append(chave)

    repetidas = conflitos = 0
    for item in novos:
        chave = normalizar(item["texto"])
        rotulo = item["intencao"]
        if not chave:
            repetidas += 1
            continue
        if chave in rotulos_exatos:
            if rotulos_exatos[chave] != rotulo:
                conflitos += 1
            else:
                repetidas += 1
            continue
        anteriores = por_rotulo.setdefault(rotulo, [])
        if any(SequenceMatcher(None, chave, anterior).ratio() >= limiar for anterior in anteriores):
            repetidas += 1
            continue
        aceitos.append(item)
        anteriores.append(chave)
        rotulos_exatos[chave] = rotulo
    return aceitos, repetidas, conflitos


def salvar_csv(caminho: Path, linhas: list[dict]) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(linhas, columns=COLUNAS)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="", delete=False,
                                     dir=caminho.parent, suffix=".tmp") as temporario:
        temporario_path = Path(temporario.name)
        df.to_csv(temporario, index=False)
    os.replace(temporario_path, caminho)


def carregar_existentes(caminho: Path) -> list[dict]:
    if not caminho.exists():
        return []
    df = pd.read_csv(caminho, dtype=str, keep_default_na=False)
    faltantes = set(COLUNAS) - set(df.columns)
    if faltantes:
        raise ValueError(f"CSV existente sem colunas obrigatórias: {sorted(faltantes)}")
    return df[COLUNAS].to_dict("records")


def registrar_prompts(caminho: Path, modelo: str, logs: list[dict], total: int,
                      aceitas: int, repetidas: int, conflitos: int) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with caminho.open("a", encoding="utf-8") as arquivo:
        if caminho.stat().st_size == 0:
            arquivo.write("# Registro de geração de dados com a API oficial da OpenAI\n")
        arquivo.write(
            f"\n## {datetime.now().astimezone():%d/%m/%Y %H:%M %Z} — modelo {modelo}\n\n"
            f"- Candidatas: {total}; aceitas: {aceitas}\n"
            f"- Duplicadas removidas: {repetidas}; conflitos entre rótulos: {conflitos}\n"
        )
        for log in logs:
            arquivo.write(
                f"\n### {log['rotulo']} — {log['estilo']}\n\n"
                f"- Frases utilizadas: {log['quantidade']}; tentativas: {log['tentativas']}\n\n"
                f"~~~text\n{log['prompt']}\n~~~\n"
            )


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--testar-conexao", action="store_true",
                        help="faz uma chamada curta para validar chave, modelo e API")
    parser.add_argument("--rotulos", nargs="*", default=None)
    parser.add_argument("--n", type=int, default=FRASES_POR_ESTILO,
                        help="quantidade por estilo e por intenção")
    parser.add_argument("--saida", default=ARQUIVO_SAIDA)
    args = parser.parse_args(argv)

    chave = obter_chave()
    if not chave:
        print(f"[ERRO] Chave não encontrada. Adicione {CHAVE_ENV}=... ao .env.")
        return 1
    try:
        cliente = criar_cliente(chave)
        if args.testar_conexao:
            mensagem = testar_conexao(cliente)
            print(f"[OK] Conexão com a API oficial da OpenAI confirmada. Modelo: {MODELO}.")
            print(f"Resposta do modelo: {mensagem}")
            return 0

        if args.n < 1:
            print("[ERRO] --n precisa ser maior que zero.")
            return 2
        sys.path.insert(0, str(RAIZ))
        from chatbot.config import carregar_config

        config = carregar_config(str(RAIZ / "grupo.yaml"))
        rotulos = args.rotulos if args.rotulos is not None else ROTULOS_PADRAO
        if rotulos is None:
            rotulos = list(config.nomes_intencoes) + ["chitchat", "fora_dominio"]
        validos = set(config.nomes_intencoes) | {"chitchat", "fora_dominio"}
        invalidos = sorted(set(rotulos) - validos)
        if invalidos:
            print(f"[ERRO] Rótulos desconhecidos: {invalidos}. Válidos: {sorted(validos)}")
            return 2

        candidatos: list[dict] = []
        logs: list[dict] = []
        for rotulo in rotulos:
            for estilo in ESTILOS:
                frases, prompt, tentativas = gerar_lote(
                    cliente, config, rotulo, estilo, args.n
                )
                candidatos.extend(
                    {"texto": frase, "intencao": rotulo, "origem": "llm"}
                    for frase in frases
                )
                logs.append({"rotulo": rotulo, "estilo": estilo,
                             "quantidade": len(frases), "tentativas": tentativas,
                             "prompt": prompt})
                print(f"  {rotulo:18s} | {len(frases):3d}/{args.n} | {estilo[:48]}")

        saida = Path(args.saida)
        if not saida.is_absolute():
            saida = RAIZ / saida
        existentes = carregar_existentes(saida)
        aceitos, repetidas, conflitos = deduplicar(candidatos, existentes)
        todos = existentes + aceitos
        salvar_csv(saida, todos)
        registrar_prompts(RAIZ / ARQUIVO_PROMPTS, MODELO, logs, len(candidatos),
                          len(aceitos), repetidas, conflitos)
        print(f"\n[OK] {len(aceitos)} novas frases adicionadas em {saida}.")
        print(f"Repetidas: {repetidas} | conflitos de rótulo: {conflitos} | total: {len(todos)}")
        print("Revise manualmente os dados antes de copiá-los para dados/treino.csv.")
        print("Nunca utilize frases geradas no conjunto dados/teste.csv.")
        return 0
    except Exception as erro:
        try:
            from openai import OpenAIError
            if isinstance(erro, OpenAIError):
                print(f"[ERRO API OpenAI] {erro}")
                return 1
        except ImportError:
            pass
        print(f"[ERRO] {erro}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
