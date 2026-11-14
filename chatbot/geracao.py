"""Geração controlada de frases de treino com JSON via OpenRouter."""
from __future__ import annotations

import json
import re
import unicodedata
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path

import pandas as pd

from .config import Config
from .llm import ClienteLLM

ESTILOS = [
    "perguntas completas e educadas",
    "mensagens curtas e informais, com abreviações naturais",
    "mensagens com erros leves de digitação, acentuação ou pontuação",
    "mensagens contextualizadas, como alguém explicando sua situação",
    "mensagens muito curtas, de 1 a 4 palavras",
]


def _descricao(config: Config, rotulo: str) -> str:
    if rotulo == "chitchat":
        return (
            "conversa social: cumprimentos, agradecimentos, despedidas, confirmações, "
            "elogios, risadas e perguntas sobre o próprio chatbot; sem pedidos de informação"
        )
    if rotulo == "fora_dominio":
        return (
            f"assuntos que o chatbot NÃO atende. O chatbot atende somente {config.tema} "
            f"({config.assuntos()}). Inclua negativos difíceis sobre outros serviços universitários "
            "e temas cotidianos, mas nunca dúvidas sobre o Mercado Escola"
        )
    return config.intencoes[rotulo].descricao


def _prompt(config: Config, rotulo: str, quantidade: int, estilo: str) -> str:
    outras = [
        info.descricao for nome, info in config.intencoes.items()
        if nome != rotulo
    ]
    restricao = ""
    if rotulo not in {"chitchat", "fora_dominio"} and outras:
        restricao = "\nNão gere perguntas sobre estas outras intenções: " + "; ".join(outras) + "."

    return f"""Gere dados sintéticos para treinar um classificador de intenções de um chatbot brasileiro.

O chatbot atende exclusivamente dúvidas sobre: {config.tema}.
Rótulo que deve ser gerado: {rotulo}.
Significado do rótulo: {_descricao(config, rotulo)}.
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

Retorne exclusivamente um objeto JSON válido neste formato:
{{"frases": ["mensagem 1", "mensagem 2"]}}
Não use Markdown nem texto fora do JSON."""


def _normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFKC", texto).casefold()
    texto = re.sub(r"[^\w\s]", " ", texto, flags=re.UNICODE)
    return " ".join(texto.split())


def _ler_json(resposta: str) -> list[str]:
    bruto = resposta.strip()
    inicio, fim = bruto.find("{"), bruto.rfind("}")
    if inicio < 0 or fim <= inicio:
        raise ValueError("resposta sem objeto JSON")
    objeto = json.loads(bruto[inicio:fim + 1])
    if not isinstance(objeto, dict) or not isinstance(objeto.get("frases"), list):
        raise ValueError('JSON deve conter a lista "frases"')
    frases = []
    for item in objeto["frases"]:
        if isinstance(item, str):
            frase = " ".join(item.strip().strip('"').split())
            if 3 <= len(frase) <= 300 and not frase.startswith(("-", "*")):
                frases.append(frase)
    if not frases:
        raise ValueError("JSON sem frases válidas")
    return frases


def _deduplicar(registros: list[dict], limiar: float = 0.94):
    """Deduplica por texto normalizado e similaridade, preservando a primeira ocorrência."""
    aceitos = []
    rotulos_por_texto: dict[str, str] = {}
    textos_por_rotulo: dict[str, list[str]] = {}
    duplicadas = conflitos = 0
    for item in registros:
        chave = _normalizar(item["texto"])
        if not chave:
            continue
        rotulo = item["intencao"]
        if chave in rotulos_por_texto:
            if rotulos_por_texto[chave] != rotulo:
                conflitos += 1
            else:
                duplicadas += 1
            continue
        anteriores = textos_por_rotulo.setdefault(rotulo, [])
        if any(SequenceMatcher(None, chave, anterior).ratio() >= limiar for anterior in anteriores):
            duplicadas += 1
            continue
        rotulos_por_texto[chave] = rotulo
        anteriores.append(chave)
        aceitos.append(item)
    return aceitos, duplicadas, conflitos


def gerar(
    config: Config,
    cliente: ClienteLLM,
    rotulos: list[str],
    n_por_estilo: int = 10,
    estilos: list[str] | None = None,
    registro: str | Path | None = None,
    tentativas_json: int = 3,
    limiar_similaridade: float = 0.94,
) -> pd.DataFrame:
    if n_por_estilo < 1 or tentativas_json < 1:
        raise ValueError("quantidade e tentativas precisam ser maiores que zero")
    if not 0 <= limiar_similaridade <= 1:
        raise ValueError("limiar de similaridade deve estar entre 0 e 1")

    estilos = estilos or ESTILOS
    candidatos = []
    logs = []
    for rotulo in rotulos:
        for estilo in estilos:
            prompt = _prompt(config, rotulo, n_por_estilo, estilo)
            frases = []
            erros = []
            for tentativa in range(1, tentativas_json + 1):
                try:
                    resposta = cliente.conversar(
                        [{"role": "user", "content": prompt}],
                        temperatura=0.85,
                        max_tokens=max(500, 80 * n_por_estilo),
                        response_format={"type": "json_object"},
                    )
                    frases = _ler_json(resposta)
                    if len(frases) < n_por_estilo:
                        raise ValueError(
                            f"modelo retornou {len(frases)} frases; eram esperadas {n_por_estilo}"
                        )
                    break
                except (ValueError, json.JSONDecodeError) as erro:
                    erros.append(f"tentativa {tentativa}: {erro}")
            if not frases:
                raise RuntimeError(
                    f"Falha ao receber JSON válido para {rotulo}/{estilo}: " + " | ".join(erros)
                )
            usadas = frases[:n_por_estilo]
            candidatos.extend(
                {"texto": frase, "intencao": rotulo, "origem": "llm"}
                for frase in usadas
            )
            logs.append((rotulo, estilo, prompt, len(frases), len(usadas), len(erros) + 1))
            print(f"  {rotulo:20s} | {len(usadas):3d}/{n_por_estilo} frases | {estilo[:45]}")

    aceitos, duplicadas, conflitos = _deduplicar(candidatos, limiar_similaridade)
    df = pd.DataFrame(aceitos, columns=["texto", "intencao", "origem"])

    if registro:
        caminho = Path(registro)
        caminho.parent.mkdir(parents=True, exist_ok=True)
        novo = not caminho.exists()
        with caminho.open("a", encoding="utf-8") as arquivo:
            if novo:
                arquivo.write(
                    "# Registro de geração de dados com LLM\n\n"
                    "Gerado por scripts/gerar_dados_llm.py. Use na declaração de uso de IA.\n"
                )
            arquivo.write(
                f"\n## {datetime.now().astimezone():%d/%m/%Y %H:%M %Z} — modelo {cliente.modelo}\n\n"
                f"- Formato: JSON estruturado (json_object)\n"
                f"- Candidatas: {len(candidatos)}; aceitas: {len(df)}\n"
                f"- Duplicatas/quase duplicatas removidas: {duplicadas}\n"
                f"- Conflitos exatos entre rótulos removidos: {conflitos}\n"
                f"- Limiar de similaridade: {limiar_similaridade:.2f}\n"
            )
            for rotulo, estilo, prompt, retornadas, usadas, tentativas in logs:
                arquivo.write(
                    f"\n### {rotulo} — {estilo}\n\n"
                    f"- Retornadas: {retornadas}; utilizadas: {usadas}; tentativas: {tentativas}\n\n"
                    f"~~~text\n{prompt}\n~~~\n"
                )
    print(f"  Deduplicação: {duplicadas} repetidas; {conflitos} conflitos entre rótulos.")
    return df
