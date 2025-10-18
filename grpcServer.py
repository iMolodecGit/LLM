import grpc
from concurrent import futures
from _grpc import warehouse_pb2_grpc
from src.llm_service import LLMServiceServicer

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    warehouse_pb2_grpc.add_LLMServiceServicer_to_server(LLMServiceServicer(), server)
    server.add_insecure_port("[::]:50051")
    print("🚀 gRPC server running on port 50051...")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
