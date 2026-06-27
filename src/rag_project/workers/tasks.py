from pathlib import Path

from rag_project.database.connection import SessionLocal
from rag_project.observability import get_logger
from rag_project.services.ingestion_service import IngestionService
from rag_project.workers.celery_app import celery_app


logger = get_logger(__name__)


@celery_app.task(
    name="process_document",
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3},
    retry_backoff=True,
)
def process_document(file_path: str) -> None:
    logger.info("Document processing task started: %s", file_path)
    session = SessionLocal()

    try:
        ingestion_service = IngestionService(session)
        ingestion_service.ingest(Path(file_path))
        logger.info("Document processing task succeeded: %s", file_path)
    except Exception:
        logger.exception("Document processing task failed: %s", file_path)
        raise
    finally:
        session.close()
