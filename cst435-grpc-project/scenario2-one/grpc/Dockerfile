# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy code
COPY . .

# Install dependencies
RUN pip install --no-cache-dir grpcio grpcio-tools

# Expose gRPC port
EXPOSE 50051

# Generate gRPC stubs if not copied
RUN python -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. compute.proto

# Run server
CMD ["python", "grpc_server.py"]
