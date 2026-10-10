
import csv
import json
import logging
from pathlib import Path

def configurar_log():
	caminho = Path(__file__).resolve().parent / "processamento.log"

	logging.basicConfig(
		filename=caminho,
		level=logging.INFO,
		format="%(asctime)s - %(levelname)s - %(message)s",
		encoding="utf-8"
	)

def carregar_solicitacoes():
	caminho = Path(__file__).resolve().parent / "solicitacoes.json"

	try:
		with open(caminho, "r", encoding="utf-8") as arquivo:
			solicitacoes = json.load(arquivo)

		if not isinstance(solicitacoes, list):
			raise ValueError("O arquivo JSON deve conter uma lista de solicitações.")

		return solicitacoes

	except FileNotFoundError:
		logging.error("Arquivo solicitacoes.json não encontrado.")
		print("Erro: arquivo solicitacoes.json não encontrado.")

	except json.JSONDecodeError as erro:
		logging.error(f"Arquivo JSON inválido: {erro}")
		print("Erro: o arquivo JSON possui um formato inválido.")

	except(OSError, UnicodeDecodeError, ValueError) as erro:
		logging.error(f"Erro ao carregar solicitações: {erro}")
		print(f"Erro ao carregar solicitações: {erro}")

	return None

def filtrar_aprovados(solicitacoes):
	aprovados = []
	ignorados = []

	for solicitacao in solicitacoes:
		if not isinstance(solicitacao, dict):
			ignorados.append(("Desconhecido", "Registro inválido"))
			continue

		id_solicitacao = solicitacao.get("id")
		nome = solicitacao.get("nome")
		cpf = solicitacao.get("cpf")
		status = solicitacao.get("status")

		if id_solicitacao is None or not isinstance(nome,str) or not nome.strip():
			ignorados.append((id_solicitacao, "ID ou nome ausente ou inválido"))
			continue

		if status != "APROVADO":
			ignorados.append((id_solicitacao, "Status diferente de APROVADO"))
			continue

		if not isinstance(cpf, str) or not cpf.strip():
			ignorados.append((id_solicitacao, "CPF ausente ou vazio"))
			continue

		aprovados.append({
			"id": id_solicitacao,
			"nome": nome,
			"cpf": cpf
		})

	for id_solicitacao, motivo in ignorados:
		logging.warning(
			f"Solicitação {id_solicitacao} ignorada: {motivo}"
		)
	return aprovados, ignorados

def gerar_csv(aprovados):
	caminho = Path(__file__).resolve().parent / "aprovados.csv"

	try:
		with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
			colunas = ["id", "nome", "cpf"]

			escritor = csv.DictWriter(
				arquivo,
				fieldnames=colunas,
				delimiter=","
			)

			escritor.writeheader()
			escritor.writerows(aprovados)

		logging.info(f"Arquivo CSV gerado: {caminho.name}")
		return True

	except(OSError, csv.Error) as erro:
		logging.error(f"Erro ao gerar arquivo CSV: {erro}")
		print(f"Erro ao gerar o arquivo CSV dos usuários APROVADOS: {erro}")
		return False

def main():
	configurar_log()

	logging.info("Início do processamento.")

	solicitacoes = carregar_solicitacoes()

	if solicitacoes is None:
		logging.error("Processamento interrompido: falha na leitura do JSON.")
		return
	aprovados, ignorados = filtrar_aprovados(solicitacoes)

	logging.info(f"Total de registros lidos: {len(solicitacoes)}")
	logging.info(f"Total de registros aprovados: {len(aprovados)}")
	logging.info(f"Total de registros ignorados: {len(ignorados)}")

	print(f"Total de registros lidos: {len(solicitacoes)}")
	print(f"Total de registros aprovados: {len(aprovados)}")
	print(f"Total de registros ignorados: {len(ignorados)}")

	if gerar_csv(aprovados):
		logging.info(f"Total de registros exportados: {len(aprovados)}")
		print("Arquivo aprovados.csv gerado com sucesso.")
	else:
		logging.error("Processamento interrompido: falha na geração do CSV.")
		return

	logging.info("Processamento concluído com sucesso.")


if __name__ == "__main__":
	main()
