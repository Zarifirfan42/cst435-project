FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir grpcio grpcio-tools
RUN python -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. compute.proto
EXPOSE 50051
CMD ["python", "grpc_server.py"]
