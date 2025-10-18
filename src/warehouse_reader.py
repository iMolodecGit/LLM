import os
import pandas as pd

def read_warehouse_excel() -> pd.DataFrame:
    """Загружает таблицу склада"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(base_dir, "../data/warehouse.xlsx")
    return pd.read_excel(excel_path)
