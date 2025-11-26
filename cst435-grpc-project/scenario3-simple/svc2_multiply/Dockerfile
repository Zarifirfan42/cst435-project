FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install grpcio grpcio-tools
EXPOSE 50052
CMD ["python", "svc2_server.py"]
