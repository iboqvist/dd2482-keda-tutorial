FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir pika

COPY producer.py .
COPY worker.py .

CMD ["python", "worker.py"]