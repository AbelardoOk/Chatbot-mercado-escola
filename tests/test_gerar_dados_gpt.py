import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "gerar_dados_gpt.py"
spec = importlib.util.spec_from_file_location("gerar_dados_gpt", SCRIPT)
gpt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gpt)


class TestGerarDadosGPT(unittest.TestCase):
    def test_ler_env_com_nome_solicitado(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = Path(tmp) / ".env"
            env.write_text('open_api_key="sk-teste-123"\n', encoding="utf-8")
            with patch.dict(os.environ, {}, clear=True):
                self.assertEqual(gpt.obter_chave(env), "sk-teste-123")

    def test_json_valido(self):
        frases = gpt.ler_frases_json('{"frases": ["Qual o horário?", "Onde fica a feira?"]}')
        self.assertEqual(len(frases), 2)

    def test_json_invalido_e_rejeitado(self):
        with self.assertRaises((json.JSONDecodeError, ValueError)):
            gpt.ler_frases_json('{"itens": []}')

    def test_deduplicacao_e_conflito(self):
        antigos = [{"texto": "Qual o horário da feira?", "intencao": "horario", "origem": "manual"}]
        novos = [
            {"texto": "Qual o horário da feira?", "intencao": "horario", "origem": "gpt"},
            {"texto": "Qual o horário da feira?", "intencao": "localizacao", "origem": "gpt"},
            {"texto": "Onde fica o mercado escola?", "intencao": "localizacao", "origem": "gpt"},
        ]
        aceitos, repetidas, conflitos = gpt.deduplicar(novos, antigos)
        self.assertEqual(len(aceitos), 1)
        self.assertEqual(repetidas, 1)
        self.assertEqual(conflitos, 1)

    def test_solicitar_json_chama_sdk_com_json_mode(self):
        fake = Mock()
        fake.chat.completions.create.return_value = SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content='{"frases": ["Que horas abre?"]}'))]
        )
        retorno = gpt.solicitar_json(fake, "Gere JSON", modelo="modelo-teste")
        self.assertIn('"frases"', retorno)
        kwargs = fake.chat.completions.create.call_args.kwargs
        self.assertEqual(kwargs["model"], "modelo-teste")
        self.assertEqual(kwargs["response_format"], {"type": "json_object"})

    def test_teste_conexao_com_resposta_simulada(self):
        fake = Mock()
        fake.chat.completions.create.return_value = SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content='{"status":"ok","mensagem":"Conectado"}'))]
        )
        self.assertEqual(gpt.testar_conexao(fake, "modelo-teste"), "Conectado")
        fake.chat.completions.create.assert_called_once()

    def test_salvar_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            destino = Path(tmp) / "dados" / "saida.csv"
            gpt.salvar_csv(destino, [{"texto": "Oi", "intencao": "chitchat", "origem": "llm"}])
            self.assertTrue(destino.exists())
            self.assertIn("chitchat", destino.read_text(encoding="utf-8"))
            self.assertIn(",llm", destino.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
