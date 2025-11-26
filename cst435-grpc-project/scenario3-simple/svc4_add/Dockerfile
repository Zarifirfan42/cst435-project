FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install grpcio grpcio-tools
EXPOSE 50054
CMD ["python", "svc4_server.py"]
