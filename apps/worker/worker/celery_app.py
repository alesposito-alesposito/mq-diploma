from celery import Celery
import os

redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery_app = Celery(
    "mail_worker",
    broker=redis_url,
    backend=redis_url,
)
