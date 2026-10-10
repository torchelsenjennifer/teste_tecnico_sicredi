# Teste Técnico Sicredi — Processamento de Solicitações

## Descrição

Aplicação desenvolvida em Python para automatizar o processamento de solicitações de cadastro recebidas por meio de um arquivo JSON.

O sistema realiza a leitura dos registros, identifica solicitações aprovadas com CPF preenchido e gera um arquivo CSV com os dados selecionados.

Durante a execução, também são registrados logs com informações do processamento, solicitações ignoradas e possíveis erros.

## Tecnologias utilizadas

- Python 3.10.6
- Bibliotecas nativas: `json`, `csv`, `logging` e `pathlib`
- `unittest`, `unittest.mock` e `tempfile` para testes automatizados
- Git para versionamento do projeto

Não são necessárias bibliotecas externas.

## Estrutura do projeto

- `main.py`: responsável pela leitura, validação, filtragem e exportação dos dados.
- `test_main.py`: contém os testes automatizados.
- `solicitacoes.json`: arquivo de entrada fornecido para o teste técnico.
- `README.md`: documentação do projeto, contendo instruções de execução, regras de processamento e decisões técnicas.
- `.gitignore`: define arquivos que não devem ser versionados.
- `aprovados.csv`: arquivo gerado durante a execução.
- `processamento.log`: arquivo que registra os eventos do processamento.

## Pré-requisitos

- Python 3.10 ou superior (desenvolvido e testado com Python 3.10.6).
- Terminal para executar os comandos.

## Como executar

**1. Obter o projeto**

Baixar o arquivo `.zip` e descompactá-lo no computador ou clonar o repositório do GitHub:

```bash
git clone https://github.com/torchelsenjennifer/teste_tecnico_sicredi.git
```

**2. Acessar a pasta do projeto**

```bash
cd teste_tecnico_sicredi
```

**3. Confirmar o arquivo de entrada**

Verificar se o arquivo `solicitacoes.json` está na mesma pasta do `main.py`.

**4. Executar a aplicação**

```bash
python main.py
```

Após a execução, serão gerados os arquivos `aprovados.csv` e `processamento.log`.

## Regras de processamento

Uma solicitação será exportada quando:

- Possuir status igual a `APROVADO`.
- Possuir CPF preenchido.
- Possuir ID e nome válidos conforme as verificações implementadas.

Registros que não atendam às condições serão ignorados e terão seus motivos registrados no log.

Não é realizada a validação dos dígitos verificadores do CPF, conforme orientação do teste técnico.

## Arquivo CSV

O arquivo `aprovados.csv` é gerado utilizando:

- Codificação UTF-8.
- Vírgula como separador.
- Colunas `id`, `nome` e `cpf`.
- Cabeçalho na primeira linha.

A cada execução bem-sucedida, o arquivo anterior é sobrescrito.

## Tratamento de erros e logs

A aplicação trata situações como:

- Arquivo JSON não encontrado.
- Conteúdo JSON inválido.
- Estrutura principal incompatível com uma lista.
- Registros incompletos ou inválidos.
- Falhas de escrita na geração do CSV.

O arquivo `processamento.log` contém data e horário, nível da mensagem e descrição do evento.

São registrados o início da execução, as solicitações ignoradas, os totais processados, os erros identificados e a conclusão do processamento.

São utilizados diferentes níveis de log:

- `INFO`: informações sobre a execução e os resultados.
- `WARNING`: solicitações ignoradas durante a filtragem.
- `ERROR`: falhas identificadas durante o processamento.

## Testes automatizados

Foram implementados 10 testes automatizados utilizando a biblioteca nativa `unittest`, contemplando:

- Solicitações aprovadas.
- Solicitações pendentes.
- CPF vazio ou nulo.
- Registros com campos obrigatórios ausentes.
- Lista de solicitações vazia.
- Arquivo JSON não encontrado.
- Conteúdo JSON inválido.
- Geração e leitura do arquivo CSV.
- Simulação de erro durante a geração do CSV.

Para executar os testes:

```bash
python -m unittest -v
```

## Premissas e decisões técnicas

- O arquivo de entrada deve conter uma lista JSON de solicitações.
- O status é comparado exatamente com o valor `APROVADO`.
- O CPF é tratado como texto, preservando possíveis zeros à esquerda.
- Valores de CPF nulos, vazios ou compostos somente por espaços são ignorados.
- ID e nome são considerados campos necessários para exportação.
- O projeto utiliza somente bibliotecas nativas para reduzir dependências.
- O código foi organizado em funções com responsabilidades específicas, facilitando a manutenção e os testes.
- Os arquivos de saída e log não são versionados, pois são produzidos automaticamente.

## Integração com BPM

Em um processo de BPM, as solicitações poderiam ser recebidas por meio de um formulário, substituindo a entrada dos dados por arquivo JSON. Após o preenchimento, cada solicitação seguiria para uma etapa de análise, na qual um responsável poderia aprovar ou reprovar o cadastro. Após a conclusão dessa etapa, a automação Python seria acionada para processar os registros aprovados, aplicar as validações necessárias e gerar o arquivo CSV para utilização pelas demais áreas.

Os registros ignorados e possíveis falhas seriam registrados em log, permitindo o acompanhamento e a rastreabilidade do processamento.

Relacionando essa proposta com minha experiência profissional, atualmente trabalho no desenvolvimento de um sistema de gestão de saúde que possui diferentes fluxos de cadastro, validação de informações e processamento de registros conforme regras de negócio. Embora sejam contextos diferentes, a lógica de organizar etapas, validar condições e executar ações de acordo com a situação de cada registro é semelhante à que aplicaria nessa integração com BPM.

## Ferramentas de consulta e inteligência artificial

ChatGPT (OpenAI): utilizado como apoio na compreensão da sintaxe Python, revisão da documentação, dicas para deixar melhor a leitura/organização do código e exemplos para tentar gerar erros na aplicação.

Google: utilizado para pesquisar conceitos, exemplos de utilização e esclarecer dúvidas sobre determinadas funções e recursos da linguagem Python.

Documentação oficial do Python: consultada para compreender o funcionamento de recursos e bibliotecas nativas utilizadas no projeto, especialmente em situações em que precisava entender melhor sua aplicação. https://docs.python.org/3.10/