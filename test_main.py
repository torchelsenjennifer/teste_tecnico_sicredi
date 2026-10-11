import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from main import carregar_solicitacoes,filtrar_aprovados, gerar_csv, main

class TestFiltrarAprovados(unittest.TestCase):

	def test_arquivo_nao_encontrado(self):
		with patch("main.Path") as caminho_simulado:
			caminho_simulado.return_value.resolve.return_value.parent.__truediv__.return_value = Path(
				"arquivo_inexistente.json"
			)

			solicitacoes = carregar_solicitacoes()

		self.assertIsNone(solicitacoes)

	def test_json_invalido(self):
		with tempfile.TemporaryDirectory() as diretorio:
			caminho = Path(diretorio) / "solicitacoes.json"
			caminho.write_text("{json invalido", encoding="utf-8")

			with patch("main.Path") as caminho_simulado:
				caminho_simulado.return_value.resolve.return_value.parent.__truediv__.return_value = caminho

				solicitacoes = carregar_solicitacoes()

		self.assertIsNone(solicitacoes)

	def test_solicitacao_aprovado(self):
		solicitacoes = [
			{
				"id": 1,
				"nome": "Maria Silva",
				"cpf": "12345678900",
				"status": "APROVADO"
			}
		]

		aprovados, ignorados = filtrar_aprovados(solicitacoes)

		self.assertEqual(len(aprovados), 1)
		self.assertEqual(len(ignorados), 0)

	def test_solicitacao_pendente(self):
		solicitacoes = [
			{
				"id": 2,
				"nome": "João Souza",
				"cpf": "12345678900",
				"status": "PENDENTE"
			}
		]

		aprovados, ignorados = filtrar_aprovados(solicitacoes)

		self.assertEqual(len(aprovados), 0)
		self.assertEqual(len(ignorados), 1)

	def test_id_vazio(self):
		solicitacoes = [
			{
				"id": "",
				"nome": "Maria Silva",
				"cpf": "12345678900",
				"status": "APROVADO"
			}
		]

		aprovados, ignorados = filtrar_aprovados(solicitacoes)

		self.assertEqual(len(aprovados), 0)
		self.assertEqual(len(ignorados), 1)
		self.assertEqual(ignorados[0][1], "ID ou nome ausente ou inválido")

	def test_id_com_espacos(self):
		solicitacoes = [
			{
				"id": "   ",
				"nome": "João Souza",
				"cpf": "12345678900",
				"status": "APROVADO"
			}
		]

		aprovados, ignorados = filtrar_aprovados(solicitacoes)

		self.assertEqual(len(aprovados), 0)
		self.assertEqual(len(ignorados), 1)
		self.assertEqual(
			ignorados[0][1],
			"ID ou nome ausente ou inválido"
		)

	def test_cpf_vazio(self):
		solicitacoes = [
			{
				"id": 3,
				"nome": "Ana Oliveira",
				"cpf": "",
				"status": "APROVADO"
			}
		]

		aprovados, ignorados = filtrar_aprovados(solicitacoes)

		self.assertEqual(len(aprovados), 0)
		self.assertEqual(len(ignorados), 1)
		self.assertEqual(
			ignorados[0][1],
			"CPF ausente ou vazio"
		)

	def test_cpf_nulo (self):
		solicitacoes = [
			{
				"id": 4,
				"nome": "Pedro Santos",
				"cpf": None,
				"status": "APROVADO"
			}
		]

		aprovados, ignorados = filtrar_aprovados(solicitacoes)

		self.assertEqual(len(aprovados), 0)
		self.assertEqual(len(ignorados), 1)

	def test_campo_obrigatorio_ausente(self):
		solicitacoes = [
			{
				"id": 5,
				"cpf": "12345678900",
				"status": "APROVADO"
			}
		]

		aprovados, ignorados = filtrar_aprovados(solicitacoes)

		self.assertEqual(len(aprovados), 0)
		self.assertEqual(len(ignorados), 1)
		self.assertEqual(
			ignorados[0][1],
			"ID ou nome ausente ou inválido"
		)

	def test_lista_vazio(self):
		aprovados, ignorados = filtrar_aprovados([])

		self.assertEqual(len(aprovados), 0)
		self.assertEqual(len(ignorados), 0)

class TestGerarCSV(unittest.TestCase):

	def test_gerar_csv(self):
		aprovados = [
			{
				"id": 1,
				"nome": "Maria Silva",
				"cpf": "01234567890"
			}
		]

		with tempfile.TemporaryDirectory() as directorio:
			caminho = Path(directorio) / "aprovados.csv"

			with patch("main.Path") as caminho_simulado:
				caminho_simulado.return_value.resolve.return_value.parent.__truediv__.return_value = caminho

				resultado = gerar_csv(aprovados)

			self.assertTrue(resultado)

			with open(caminho, "r", encoding="utf-8", newline="") as arquivo:
				registro = list(csv.DictReader(arquivo))

			self.assertEqual(len(registro), 1)
			self.assertEqual(registro[0]["nome"], "Maria Silva")
			self.assertEqual(registro[0]["cpf"], "01234567890")

	def test_erro_ao_gerar_csv(self):
		aprovados = [
			{
				"id": 1,
				"nome": "Maria Silva",
				"cpf": "12345678900"
			}
		]

		with tempfile.TemporaryDirectory() as diretorio:
			caminho = Path(diretorio) / "aprovados.csv"

			caminho.mkdir()

			with patch("main.Path") as caminho_simulado:
				caminho_simulado.return_value.resolve.return_value.parent.__truediv__.return_value = caminho

				resultado = gerar_csv(aprovados)

		self.assertFalse(resultado)

class TestMain(unittest.TestCase):

	def test_processamento_sucesso(self):
		solicitacoes = [
			{
				"id": 1,
				"nome": "Maria Silva",
				"cpf": "12345678900",
				"status": "APROVADO"
			}
		]

		with patch("main.configurar_log"), \
			patch("main.carregar_solicitacoes", return_value=solicitacoes), \
			patch("main.gerar_csv", return_value=True):

			resultado = main()

		self.assertEqual(resultado, 0)

	def test_processamento_erro_csv(self):
		solicitacoes = [
			{
				"id": 1,
				"nome": "Maria Silva",
				"cpf": "12345678900",
				"status": "APROVADO"
			}
		]

		with patch("main.configurar_log"), \
			patch("main.carregar_solicitacoes", return_value=solicitacoes), \
			patch("main.gerar_csv", return_value=False):

			resultado = main()

		self.assertEqual(resultado, 1)

if __name__ == "__main__":
	unittest.main()
