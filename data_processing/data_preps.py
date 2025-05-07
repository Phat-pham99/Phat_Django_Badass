import re
import pandas as pd
from pandas import DataFrame
from datetime import datetime
from sqlalchemy import create_engine, text

def load_data():
    #--------------------------------------------------------#
    SHEET_ARCHIVED = "1ztPEmbACo0ytUy0unMmF1qtYqvWf6Dq2RoyK2w_mjcw"
    # SHEET_ID = "1eYNEUqr0q8L2YYa_ZVR1yg8rKjphzVg8WopgjtICCwo"
    # SHEET_2024 = "1F6X0dxAtKfK0gChnakYa80dofVoyt42oL13urbgegzw"
    # SHEET_2025 = "1XJU6FDHbDWk261xwy96zhv4qa92JLz2TjgBbjNTGbMo"
    SHEET_NAME = "expense"
    # SHEET_NAME = "dashboard"
    URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ARCHIVED}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"
    return pd.read_csv(URL)

def handle_date(date_string:str) -> datetime.date:
    """
    Something like dd/mm/yyyy -> datetime.date
    """
    return datetime.strptime(date_string, "%d/%m/%Y").date()

def data_cleaning(DataFrame:DataFrame) -> DataFrame:
    pass


def DF_2_SQL(DataFrame:DataFrame,database_name:str,table_name:str) -> None:
    engine = create_engine('sqlite:///test.db', echo=True)
    DataFrame.to_sql('Expenses', con=engine, if_exists='append')
    with engine.connect() as conn:
        conn.execute(text("SELECT * FROM Expenses")).fetchall()
        conn.commit()

if __name__ == "__main__":
    data = load_data()
    DF_2_SQL(data)