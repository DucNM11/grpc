FROM python:3.8-slim-bullseye

WORKDIR /app
COPY grpc_server.py /app/
COPY common/common.py common/service_pb2_grpc.py common/service_pb2.py /app/common/

RUN pip install --no-cache-dir grpcio==1.44.0 grpcio-tools numpy

CMD ["python", "grpc_server.py"]
EXPOSE 9999
