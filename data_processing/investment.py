import re
import numpy as np
import pandas as pd
from pandas import DataFrame
from datetime import datetime
from sqlalchemy import create_engine, text
from pprint import pprint

def load_data() -> DataFrame:
    #--------------------------------------------------------#
    SHEET_2025 = "1XJU6FDHbDWk261xwy96zhv4qa92JLz2TjgBbjNTGbMo"
    SHEET_NAME = "investment"
    URL = f"https://docs.google.com/spreadsheets/d/{SHEET_2025}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"
    return pd.read_csv(URL)

def handle_date(date_string:str) -> datetime.date:
    """
    Something like `dd thang M, YYY` -> datetime.date
    """
    date_string = date_string.replace(' tháng ','').replace(', ','')
    return datetime.strptime(date_string, "%d%m%Y").date()

def custom_date(df:DataFrame):
    temp_date_serie = []
    for item in df['date']:
        temp_date_serie.append(handle_date(item))
    df['date'] = temp_date_serie
    return df
def handle_amount(df:DataFrame,col:str):
    temp_list = []
    for item in df[col]:
        temp_list.append(
        item.replace('.','')
        )
    df[col] = temp_list
    return df
    

def custom_fillna(df:DataFrame) -> DataFrame:
    df.drop(df.columns[df.columns.str.contains(
    'unnamed', case=False)], axis=1, inplace=True)
    # df.dropna(axis='rows',how='all')
    df.dropna(axis='rows',how='all',inplace=True)
    df.dropna(axis='columns',how='all',inplace=True)
    return df

def data_cleaning(df:DataFrame)-> DataFrame:
    df = custom_fillna(df)
    df = custom_date(df)
    df = handle_amount(df,col="amount")
    df.rename(columns={'type': 'investment_type'}, inplace=True)
    df = df[['date',"investment_type",'amount']]
    return df

def DF_2_SQL(df:DataFrame,database_name:str,table_name:str) -> None:
    engine = create_engine(database_name, echo=True)
    df.to_sql(table_name, con=engine, if_exists='append', index=False)
    with engine.connect() as conn:
        conn.execute(text(f"SELECT * FROM {table_name}")).fetchall()
        conn.commit()

if __name__ == "__main__":
    data = load_data()
    data = data_cleaning(data)
    pprint(data)
    DF_2_SQL(
    df=data,
    database_name='sqlite:///db.sqlite3',
    table_name="phat_investment_investment"
    )

