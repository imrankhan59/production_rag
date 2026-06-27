from pathlib import Path

from rag_project.observability import get_logger
from rag_project.workers.publisher import TaskPublisher


logger = get_logger(__name__)


class InitialScanner:
    """
    Scans an existing directory and publishes documents for processing.

    Responsibilities:
    - Find existing PDF files
    - Publish each file path to the async pipeline

    This scanner does not:
    - Extract metadata
    - Check duplicates
    - Access the database
    - Process documents directly
    """

    def __init__(self, directory: Path) -> None:
        self._directory = directory
        self._publisher = TaskPublisher()

    def scan(self) -> None:
        logger.info("Starting initial scan: %s", self._directory)

        if not self._directory.exists():
            logger.warning("Scan directory does not exist: %s", self._directory)
            return

        if not self._directory.is_dir():
            logger.warning("Scan path is not a directory: %s", self._directory)
            return

        files = sorted(self._directory.glob("*.pdf"))

        if not files:
            logger.info("No existing PDF files found: %s", self._directory)
            return

        logger.info(
            "Found %d existing PDF file(s) for ingestion",
            len(files),
        )

        for file_path in files:
            logger.info("Publishing existing PDF for ingestion: %s", file_path)
            self._publisher.publish_document(file_path)

        logger.info("Initial scan completed: %s", self._directory)