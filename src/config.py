import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "mistralai/mistral-7b-instruct"
EXCEL_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "../data/warehouse.xlsx"
)
