# ====== CONFIG ======
PROTO_DIR = grpc_service/proto
OUT_DIR = grpc_service
SERVER = grpcServer.py
PYTHON = python3

# ====== TASKS ======

.PHONY: proto run clean

# Сгенерировать Python-код из .proto
proto:
	@echo "🛠️  Generating gRPC code from warehouse.proto..."
	python -m grpc_tools.protoc \
		-I$(PROTO_DIR) \
		--python_out=$(OUT_DIR) \
		--grpc_python_out=$(OUT_DIR) \
		$(PROTO_DIR)/warehouse.proto
	@echo "✅ Proto files generated successfully!"

# Запуск gRPC сервера
run:
	@echo "🚀 Starting gRPC server..."
	$(PYTHON) $(SERVER)

# Очистить сгенерированные файлы
clean:
	@echo "🧹 Cleaning generated files..."
	rm -f $(OUT_DIR)/warehouse_pb2.py
	rm -f $(OUT_DIR)/warehouse_pb2_grpc.py
	@echo "✅ Clean complete!"
