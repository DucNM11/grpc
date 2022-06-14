FROM python:3.8-slim-bullseye

WORKDIR /app
COPY grpc_server.py common.py service_pb2.py service_pb2_grpc.py /app/

RUN pip install --no-cache-dir grpcio==1.44.0 grpcio-tools numpy

CMD ["python", "grpc_server.py"]
EXPOSE 8888
