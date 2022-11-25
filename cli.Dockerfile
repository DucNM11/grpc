FROM python:3.8-slim-bullseye

WORKDIR /app
COPY templates/ /app/templates/
COPY client.py app.py /app/
COPY common/common.py common/service_pb2_grpc.py common/service_pb2.py /app/common/

RUN pip install --no-cache-dir grpcio==1.44.0 grpcio-tools numpy flask

CMD ["python", "-m", "flask", "--app", "app", "run", "--host=0.0.0.0"]
EXPOSE 5000
