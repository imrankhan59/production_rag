from pathlib import Path

from rag_project.observability import get_logger
from rag_project.workers.tasks import process_document


logger = get_logger(__name__)


class TaskPublisher:
    """
    Publishes document processing tasks to Celery.
    """

    @staticmethod
    def publish_document(file_path: Path) -> None:
        logger.info("Publishing document processing task: %s", file_path)
        process_document.delay(str(file_path))
        logger.info("Document processing task published: %s", file_path)
