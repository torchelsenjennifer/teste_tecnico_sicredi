
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

def main():
	solicitacoes = carregar_solicitacoes()

	if solicitacoes is not None:
		print(f"Total de registros lidos: {len(solicitacoes)}")


if __name__ == "__main__":
	main()
