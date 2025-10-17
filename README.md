# LLM

---------------
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. grpc_service/warehouse.proto
source  ./www/llm/.venv/bin/activate