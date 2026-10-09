
import json
from pathlib import Path

def carregar_solicitacoes():
	caminho = Path(__file__).resolve().parent / "solicitacoes.json"

	try:
		with open(caminho, "r", encoding="utf-8") as arquivo:
			solicitacoes = json.load(arquivo)

		return solicitacoes

	except FileNotFoundError:
		print("Erro: arquivo solicitacoes.json não encontrado.")

	except json.JSONDecodeError:
		print("Erro: o arquivo JSON possui um formato inválido.")

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

	return aprovados, ignorados

def main():
	solicitacoes = carregar_solicitacoes()

	if solicitacoes is not None:
		aprovados, ignorados = filtrar_aprovados(solicitacoes)

		print(f"Total de registros lidos: {len(solicitacoes)}")
		print(f"Total de registros aprovados: {len(aprovados)}")
		print(f"Total de registros ignorados: {len(ignorados)}")

if __name__ == "__main__":
	main()
