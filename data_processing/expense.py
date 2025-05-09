import re
import numpy as np
import pandas as pd
from pandas import DataFrame
from datetime import datetime
from sqlalchemy import create_engine, text
from pprint import pprint

def load_data():
    #--------------------------------------------------------#
    SHEET_ARCHIVED = "1ztPEmbACo0ytUy0unMmF1qtYqvWf6Dq2RoyK2w_mjcw"
    SHEET_NAME = "expense"
    URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ARCHIVED}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"
    return pd.read_csv(URL)

def handle_date(date_string:str) -> datetime.date:
    """
    Something like dd/mm/yyyy -> datetime.date
    """
    return datetime.strptime(date_string, "%d/%m/%Y").date()

def custom_date(df:DataFrame):
    temp_date_serie = []
    for item in df['date']:
        try:
            temp_date_serie.append(handle_date(item))
        except Exception as e:
            print(f"Ooh oh, {item} => {e}")
    df['date'] = temp_date_serie
    return df

def custom_fillna(df:DataFrame) -> DataFrame:
    df.drop(df.columns[df.columns.str.contains(
    'unnamed', case=False)], axis=1, inplace=True)
    # df.dropna(axis='rows',how='all')
    df.dropna(axis='rows',how='all',inplace=True)
    df.dropna(axis='columns',how='all',inplace=True)
    df['date'].bfill(axis=0,inplace=True)
    df['cash'].fillna("0.0",inplace=True)
    df['digital'].fillna("0.0",inplace=True)
    df['credit'].fillna("0.0",inplace=True)
    data['category'].fillna("others",inplace=True)
    return df

def custom_tranform_str2int(df:DataFrame) -> DataFrame:
    df['cash']=[int(item.split('.')[0])*1000 for item in data['cash']]
    df['digital']=[int(item.split('.')[0])*1000 for item in data['digital']]
    df['credit']=[int(item.split('.')[0])*1000 for item in data['credit']]
    return df

def data_cleaning(df:DataFrame)-> DataFrame:
    df = custom_fillna(df)
    df = custom_tranform_str2int(df)
    df = custom_date(df)
    return df #Đẹp trai bảnh tỏn ngay

def DF_2_SQL(df:DataFrame,database_name:str,table_name:str) -> None:
    engine = create_engine(database_name, echo=True)
    df = data_cleaning(df)
    df.to_sql(table_name, con=engine, if_exists='append', index=False)
    with engine.connect() as conn:
        conn.execute(text(f"SELECT * FROM {table_name}")).fetchall()
        conn.commit()

if __name__ == "__main__":
    data = load_data()
    data = data_cleaning(data)
    data = custom_fillna(data[1000:])
    # DF_2_SQL(
    # df=data,
    # database_name='sqlite:///db.sqlite3',
    # table_name="phat_finance_expenses"
    # )
