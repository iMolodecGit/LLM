from fastapi import FastAPI, Query
from src.llm_client import ask_llm
from src.warehouse_reader import read_warehouse_excel
from src.prompts import build_warehouse_prompt

app = FastAPI(title="LLM Warehouse Assistant API")

@app.get("/ask")
def ask_about_stock(q: str = Query(..., description="Вопрос пользователя")):
    df = read_warehouse_excel()
    products = "\n".join(
        [f"{row['Товар']} — {row['Количество']} шт (склад {row['Склад']})"
         for _, row in df.iterrows()]
    )

    prompt = build_warehouse_prompt(products, q)
    answer = ask_llm(prompt)
    return {"question": q, "answer": answer}

@app.get("/all")
def get_all():
    """Возвращает все товары"""
    df = read_warehouse_excel()
    return df.to_dict(orient="records")
