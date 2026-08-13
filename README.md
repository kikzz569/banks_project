# 🏦 Banks Project — ETL Pipeline (Maiores Bancos do Mundo por Capitalização de Mercado)

Pipeline de **ETL (Extract, Transform, Load)** em Python que extrai a lista dos maiores bancos do mundo por capitalização de mercado (em bilhões de USD), converte os valores para GBP, EUR e INR usando taxas de câmbio atualizadas, e carrega os dados processados em um arquivo CSV e em um banco de dados SQLite para consulta via SQL.

Projeto desenvolvido como exercício prático de Engenharia de Dados, simulando um cenário real: uma empresa multinacional precisa que gerentes de diferentes países consultem a capitalização de mercado dos maiores bancos na moeda local de cada região.

---

## 📌 Visão geral

O pipeline percorre as seguintes etapas:

1. **Extract** — faz scraping (via `requests` + `BeautifulSoup`) de uma tabela HTML (snapshot do Wikipedia via Wayback Machine) contendo os maiores bancos do mundo por capitalização de mercado em USD.
2. **Transform** — lê um arquivo `exchange_rate.csv` com as taxas de câmbio (EUR, GBP, INR) e cria três novas colunas no DataFrame, convertendo a capitalização de mercado de USD para cada moeda, arredondada em 2 casas decimais.
3. **Load**
   - **CSV** — salva o DataFrame transformado localmente como `largest_banks.csv`.
   - **Database** — carrega o mesmo DataFrame como uma tabela (`Largest_Banks`) em um banco SQLite (`banks.db`).
4. **Query** — executa consultas SQL sobre a tabela carregada (ex: capitalização média em GBP, top 5 bancos por nome).
5. **Logging** — todo o processo grava logs com timestamp em `code_log.txt`, permitindo rastrear cada etapa da execução (extração, transformação, carga, consultas).

---

## 🗂️ Estrutura do projeto

```
banks-project/
│
├── banks_project.py       # script principal com todo o pipeline ETL
├── exchange_rate.csv      # taxas de câmbio (USD → EUR, GBP, INR)
├── largest_banks.csv      # (gerado) saída da etapa de transformação
├── banks.db               # (gerado) banco SQLite com a tabela final
├── code_log.txt           # (gerado) log de execução com timestamps
└── README.md
```

---

## ⚙️ Tecnologias utilizadas

- **Python 3**
- **pandas** — manipulação de dados tabulares
- **numpy** — arredondamento numérico
- **BeautifulSoup + lxml** — parsing de HTML (web scraping)
- **requests** — requisições HTTP
- **sqlite3** — armazenamento e consulta em banco de dados relacional

---

## ▶️ Como executar

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/banks-project.git
cd banks-project
```

2. Instale as dependências:
```bash
pip install pandas numpy beautifulsoup4 lxml requests
```

3. Certifique-se de que o arquivo `exchange_rate.csv` está na mesma pasta do script, no formato:

| Currency | Rate |
|----------|------|
| EUR      | 0.93 |
| GBP      | 0.80 |
| INR      | 82.95 |

4. Rode o pipeline:
```bash
python banks_project.py
```

Ao final da execução, você terá:
- `largest_banks.csv` com as colunas `Name`, `MC_USD_Billion`, `MC_GBP_Billion`, `MC_EUR_Billion`, `MC_INR_Billion`
- `banks.db` contendo a tabela `Largest_Banks`
- `code_log.txt` com o histórico de execução

---

## 🔎 Exemplos de consultas executadas

```sql
SELECT * FROM Largest_Banks;

SELECT AVG(MC_GBP_Billion) FROM Largest_Banks;

SELECT Name FROM Largest_Banks LIMIT 5;
```

Essas consultas simulam o caso de uso real: gerentes regionais (Londres, Berlim, Nova Délhi) extraindo a capitalização de mercado na moeda local de sua operação.

---

## 📝 Sobre os logs

Cada etapa do pipeline (extração, transformação, carga em CSV, carga no banco, execução de queries) é registrada em `code_log.txt` com timestamp, permitindo auditar exatamente quando cada fase do processo ocorreu — prática comum em pipelines de dados de produção para debug e observabilidade.

---

## 🚀 Possíveis melhorias futuras

- Parametrizar a URL de origem e o número de bancos extraídos (atualmente limitado à tabela disponível).
- Adicionar tratamento de erros para falhas de conexão HTTP e dados ausentes na tabela HTML.
- Migrar de SQLite para um banco gerenciado (ex: PostgreSQL) para simular um ambiente produtivo.
- Adicionar testes automatizados para cada etapa do ETL (extract, transform, load).
- Orquestrar o pipeline com Airflow, incluindo agendamento e alertas de falha.

---
