FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install grpcio grpcio-tools
EXPOSE 50053
CMD ["python", "svc3_server.py"]
