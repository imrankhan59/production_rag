from pathlib import Path

from rag_project.workers.tasks import process_document


class TaskPublisher:
    """
    Publishes document processing tasks to Celery.
    """

    @staticmethod
    def publish_document(file_path: Path) -> None:
        process_document.delay(str(file_path))