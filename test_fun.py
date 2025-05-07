import pandas as pd

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

if __name__ == "__main__":
    data = load_data()
    print(data)