import pandas as pd 
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import lxml
import numpy as np 
import sqlite3

url = 'https://web.archive.org/web/20230908091635%20/https://en.wikipedia.org/wiki/List_of_largest_banks'
html_page = requests.get(url).text
soup = BeautifulSoup(html_page, 'html.parser')
db_name = 'banks.db'
table_name = 'Largest_Banks'
log_file = 'code_log.txt'
table_attributes = ['Name','MC_USD_Billion','MC_GBP_Billion','MC_EUR_Billion','MC_INR_Billion']
csv_file = 'largest_banks.csv'
conn = sqlite3.connect(db_name)
data = []


def log_progress(message):
    timestamp_format = '%Y-%m-%d %H:%M:%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    with open(log_file, "a") as f:
        f.write(timestamp + ": " + message + "\n")
    print(message)
        
def extract():
    table = soup.find_all('tbody')
    rows = table[0].find_all('tr')
    
    for row in rows:
        cols = row.find_all('td')
        if len(cols) != 0:
            name = cols[1].text
            MC_cap = cols[2].text.strip()

            data.append([name, MC_cap])
            df = pd.DataFrame(data,columns = ['Name','MC_USD_Billion'])
    return df

def transform(df):
    log_progress('Transform function started')
    exchange_rate = pd.read_csv('exchange_rate.csv')
    for index, row in exchange_rate.iterrows():
        currency = row['Currency']
        rate_value = float(row['Rate'])
        df[f"MC_{currency}_Billion"] = np.round(df['MC_USD_Billion'].astype(float) * rate_value,2)
    return df

def load_csv(df):
    df.to_csv(csv_file, index = False)

def load_db(df):
    df.to_sql(table_name, conn, if_exists='replace', index = False)

def run_queryes():
    query_statements = [f'SELECT * FROM {table_name}',
    f'SELECT AVG(MC_GBP_Billion) FROM {table_name}',
    f'SELECT name from {table_name} LIMIT 5']

    cursor = conn.cursor()
    for query in query_statements:
        cursor.execute(query)
        results = cursor.fetchall()
        print(f'Query: {query}')
        print(f'Results: {results}\n')
    
def pipeline():
    log_progress('Pipeline started')
    df = extract()
    print(df)
    log_progress('Extract function completed')
    df = transform(df)
    log_progress('Transform function completed')
    load_csv(df)
    log_progress('Load to CSV function completed')
    load_db(df)
    log_progress('Load to DB function completed')
    run_queryes()
    log_progress('Run queryes function completed')
    log_progress('Pipeline completed')

    conn.close()

pipeline()


