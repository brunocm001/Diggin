"""import pandas as pd
import numpy as np
import pyodbc
from bcpandas import SqlCreds, to_sql
from time import time
from colorama import init, Style, Fore


init(autoreset=True)

driver = pyodbc.drivers()[0]
host = 'database-1.cafpm3fc0gok.us-east-2.rds.amazonaws.com'
user = 'admin'
password = 'mdLt8mTbMSmUO345'
database = 'TestBulk'
port = 1433
uri = f'mssql+pyodbc://{user}:{password}@{host}:{port}/{database}?driver={driver}?TrustedConnection=yes'

creds = SqlCreds(
    host,
    database,
    user,
    password
)
start = time()

df = pd.read_csv('D:/1000000_lignes.csv', delimiter=',')
to_sql(df=df, table_name='10000000_lignes', creds=creds, schema='dbo', if_exists='replace', batch_size=10000, index=False)

print(Style.BRIGHT+Fore.CYAN+f'Duree de l\'insertion: '+Fore.RED+f'{round(time()-start, 2)} s')"""

print("Hello World")
