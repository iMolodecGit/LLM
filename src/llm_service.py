from _grpc import warehouse_pb2, warehouse_pb2_grpc
from src.llm_client import ask_llm
from src.warehouse_reader import read_warehouse_excel
from src.prompts import build_warehouse_prompt, build_custom_prompt

class LLMServiceServicer(warehouse_pb2_grpc.LLMServiceServicer):
    """gRPC-сервис, использующий общую бизнес-логику из core"""

    def Ask(self, request, context):
        """Ответ на вопросы по складу"""
        df = read_warehouse_excel()

        products = "\n".join(
            f"{row['Товар']} — {row['Количество']} шт (склад {row['Склад']})"
            for _, row in df.iterrows()
        )

        prompt = build_warehouse_prompt(products, request.question)
        answer = ask_llm(prompt)

        return warehouse_pb2.AskResponse(answer=answer)

    def AskScientist(self, request, context):
        """Режим с 'трамповой' персоной"""
        prompt = build_custom_prompt(request.question);

        answer = ask_llm(prompt)

        return warehouse_pb2.AskResponse(answer=answer)
