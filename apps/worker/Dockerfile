FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*
COPY apps/worker/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY apps/worker /app
ENV PYTHONPATH=/app
CMD ["celery", "-A", "worker.celery_app.celery_app", "worker", "--loglevel=INFO", "-Q", "default"]
