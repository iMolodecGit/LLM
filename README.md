# LLM

---------------
# Commands

Generate grpc metadata :  python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. grpc_service/warehouse.proto

Activate env: source ./.venv/bin/activate

Deactivate env: deactivate

Run HTTP Server command: uvicorn api.fast_server:app --reload

Run gRPC Service command: python3 grpcService.py