FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install grpcio grpcio-tools
EXPOSE 50055
CMD ["python", "svc5_server.py"]
