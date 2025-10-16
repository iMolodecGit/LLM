import os
import pandas as pd
import requests
from fastapi import FastAPI, Query
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "mistralai/mistral-7b-instruct"  # можно поменять на другую


def ask_llm(prompt: str):
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
        },
    )
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


@app.get("/ask")
def ask_about_stock(q: str = Query(..., description="Вопрос пользователя")):
    df = pd.read_excel("data/warehouse.xlsx")
    products = "\n".join(
        [f"{row['Товар']} — {row['Количество']} шт (склад {row['Склад']})"
         for _, row in df.iterrows()]
    )

    prompt = f"""
Ты помощник склада. Тебе дан список товаров с количеством на складах:

{products}

Пользователь спрашивает: "{q}"

Ответь на естественном языке: если товар есть — укажи где и сколько, 
если нет — скажи, что такого нет.
"""

    ai_response = ask_llm(prompt)
    return {"question": q, "answer": ai_response}

#============================


# from fastapi import FastAPI, Query
# import pandas as pd
# from typing import Optional
#
# app = FastAPI(title="Склад LLM API")
#
# # Загружаем Excel при старте
# DATA_FILE = "warehouse.xlsx"
# df = pd.read_excel(DATA_FILE)
#
#
# @app.get("/query")
# def query(
#     q: str = Query(..., description="Запрос: например 'шуруп', 'остатки меньше 50', 'все по складу Основной'"),
#     sklad: Optional[str] = Query(None, description="Можно указать склад"),
# ):
#     """Простой поиск по остаткам."""
#     filtered = df.copy()
#
#     # фильтр по названию
#     filtered = filtered[filtered["Товар"].str.contains(q, case=False, na=False)]
#
#     # фильтр по складу (если указан)
#     if sklad:
#         filtered = filtered[filtered["Склад"].str.contains(sklad, case=False, na=False)]
#
#     return filtered.to_dict(orient="records")
#
#
# @app.get("/all")
# def get_all():
#     """Получить все товары"""
#     return df.to_dict(orient="records")
