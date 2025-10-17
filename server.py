import os
import grpc
import pandas as pd
import requests
from concurrent import futures
from dotenv import load_dotenv

from grpc_service import warehouse_pb2, warehouse_pb2_grpc

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "mistralai/mistral-7b-instruct"

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


class LLMServiceServicer(warehouse_pb2_grpc.LLMServiceServicer):
    def Ask(self, request, context):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        excel_path = os.path.join(base_dir, "./data/warehouse.xlsx")
        print(excel_path)

        df = pd.read_excel(excel_path);
        products = "\n".join(
            [f"{row['Товар']} — {row['Количество']} шт (склад {row['Склад']})"
             for _, row in df.iterrows()]
        )

        prompt = f"""
Ты помощник склада. Тебе дан список товаров с количеством на складах:

{products}

Пользователь спрашивает: "{request.question}"

Ответь на естественном языке: если товар есть — укажи где и сколько,
если нет — скажи, что такого нет.
"""
        answer = ask_llm(prompt)
        return warehouse_pb2.AskResponse(answer=answer)

    def AskScientist(self, request, context):
            prompt = f"""
    Ты телеграм бот. К тебе приходят люди с разными вопросами.
    Пользователь спрашивает: "{request.question}"

    Ответь на естественном языке так чтоб поддержать беседу
    """
            answer = ask_llm(prompt)
            return warehouse_pb2.AskResponse(answer=answer)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    warehouse_pb2_grpc.add_LLMServiceServicer_to_server(LLMServiceServicer(), server)
    server.add_insecure_port("[::]:50051")
    print("gRPC server running on port 50051...")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
