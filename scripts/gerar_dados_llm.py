#!/usr/bin/env python3
"""Gera frases de treino em JSON estruturado via OpenRouter.

Exemplos:
    python scripts/gerar_dados_llm.py
    python scripts/gerar_dados_llm.py --rotulos horario localizacao --n 12
    python scripts/gerar_dados_llm.py --rotulos chitchat fora_dominio --n 15
    python scripts/gerar_dados_llm.py --modelo openai/gpt-4.1-mini

As frases são salvas em dados/gerados_llm.csv para revisão manual.
Nunca utilize dados gerados por LLM em dados/teste.csv.
"""
from __future__ import annotations

import argparse
import os
import sys
import tempfile
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from chatbot.config import carregar_config  # noqa: E402
from chatbot.geracao import _deduplicar, gerar  # noqa: E402
from chatbot.llm import ClienteLLM, ErroLLM  # noqa: E402

COLUNAS = ["texto", "intencao", "origem"]


def _carregar_existente(caminho: Path) -> pd.DataFrame:
    if not caminho.exists():
        return pd.DataFrame(columns=COLUNAS)
    df = pd.read_csv(caminho, dtype=str, keep_default_na=False)
    faltantes = [coluna for coluna in COLUNAS if coluna not in df.columns]
    if faltantes:
        raise ValueError(
            f"{caminho} não possui as colunas obrigatórias: {', '.join(faltantes)}"
        )
    return df[COLUNAS]


def _mesclar(antigos: pd.DataFrame, novos: pd.DataFrame, limiar: float):
    """Mantém os dados existentes como prioridade e acrescenta só frases novas."""
    registros = antigos.to_dict("records") + novos.to_dict("records")
    aceitos, repetidos, conflitos = _deduplicar(registros, limiar)
    return pd.DataFrame(aceitos, columns=COLUNAS), repetidos, conflitos


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--config", default="grupo.yaml")
    parser.add_argument("--rotulos", nargs="*", default=None)
    parser.add_argument("--n", type=int, default=10, help="frases por estilo e rótulo")
    parser.add_argument("--modelo", default=None)
    parser.add_argument("--saida", default="dados/gerados_llm.csv")
    parser.add_argument("--limiar-similaridade", type=float, default=0.94)
    parser.add_argument("--tentativas-json", type=int, default=3)
    args = parser.parse_args(argv)

    if args.n < 1 or args.tentativas_json < 1:
        parser.error("--n e --tentativas-json precisam ser maiores que zero")
    if not 0 <= args.limiar_similaridade <= 1:
        parser.error("--limiar-similaridade precisa estar entre 0 e 1")

    try:
        config = carregar_config(args.config)
        rotulos = args.rotulos or (config.nomes_intencoes + ["chitchat", "fora_dominio"])
        validos = set(config.nomes_intencoes) | {"chitchat", "fora_dominio"}
        invalidos = sorted(set(rotulos) - validos)
        if invalidos:
            print(f"[ERRO] Rótulos desconhecidos: {invalidos}. Válidos: {sorted(validos)}")
            return 2

        cliente = ClienteLLM.da_config(config)
        if args.modelo:
            cliente.modelo = args.modelo

        saida = Path(args.saida)
        if not saida.is_absolute():
            saida = config.pasta / saida
        saida.parent.mkdir(parents=True, exist_ok=True)

        print(f"Modelo: {cliente.modelo}")
        print(f"Chave: {cliente.chave_mascarada}")
        print(f"Rótulos: {', '.join(rotulos)}")
        print(f"Meta: {args.n} frases x 5 estilos por rótulo\n")

        novos = gerar(
            config,
            cliente,
            rotulos,
            n_por_estilo=args.n,
            registro=config.pasta / "dados" / "prompts_llm.md",
            tentativas_json=args.tentativas_json,
            limiar_similaridade=args.limiar_similaridade,
        )

        antigos = _carregar_existente(saida)
        resultado, repetidos, conflitos = _mesclar(
            antigos, novos, args.limiar_similaridade
        )

        # Escrita atômica para preservar o CSV anterior em caso de interrupção.
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="",
            suffix=".tmp",
            dir=saida.parent,
            delete=False,
        ) as temporario:
            caminho_temporario = Path(temporario.name)
            resultado.to_csv(temporario, index=False)
        os.replace(caminho_temporario, saida)

        print(f"\nArquivo: {saida}")
        print(f"Registros existentes: {len(antigos)}")
        print(f"Frases novas válidas: {len(novos)}")
        print(f"Novas frases adicionadas: {len(resultado) - len(antigos)}")
        print(f"Duplicatas/quase duplicatas ignoradas: {repetidos}")
        print(f"Conflitos exatos entre intenções: {conflitos}")
        print(f"Total no arquivo: {len(resultado)}")
        print(f"Consumo informado pela API: {cliente.uso}")
        print("\nRevise manualmente antes de copiar para dados/treino.csv.")
        print("Nunca utilize frases geradas por LLM em dados/teste.csv.")
        return 0
    except (ErroLLM, ValueError, RuntimeError, OSError) as erro:
        print(f"[ERRO] {erro}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
