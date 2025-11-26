FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install grpcio grpcio-tools
EXPOSE 50051
CMD ["python", "svc1_server.py"]
