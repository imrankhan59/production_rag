from celery import Celery

from rag_project.config.settings import settings


broker_url = (
    f"amqp://{settings.RABBITMQ_USER}:"
    f"{settings.RABBITMQ_PASSWORD}@"
    f"{settings.RABBITMQ_HOST}:"
    f"{settings.RABBITMQ_PORT}//"
)

celery_app = Celery(
    "rag_project",
    broker=broker_url,
    include=["rag_project.workers.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)