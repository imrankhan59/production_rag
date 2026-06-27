from pathlib import Path

from rag_project.database.connection import SessionLocal
from rag_project.services.ingestion_service import IngestionService
from rag_project.workers.celery_app import celery_app


@celery_app.task(
    name="process_document",
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3},
    retry_backoff=True,
)
def process_document(file_path: str) -> None:
    session = SessionLocal()

    try:
        ingestion_service = IngestionService(session)
        ingestion_service.ingest(Path(file_path))
    finally:
        session.close()