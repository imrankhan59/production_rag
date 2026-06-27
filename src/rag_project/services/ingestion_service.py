from pathlib import Path

from sqlalchemy.orm import Session

from rag_project.repositories.document_repository import DocumentRepository
from rag_project.schema.document import DocumentMetadata
from rag_project.services.metadata_service import MetadataService


class IngestionService:
    """
    Orchestrates the document ingestion workflow.

    Responsibilities:
    - Extract document metadata
    - Check for duplicate documents
    - Persist new documents

    This service does not:
    - Watch folders
    - Publish RabbitMQ messages
    - Run Celery tasks
    """

    def __init__(self, session: Session) -> None:
        self._session = session
        self._repository = DocumentRepository(session)

    def ingest(self, file_path: Path) -> DocumentMetadata:
        """
        Process a document and store it if it is new.

        Args:
            file_path: Path to the document.

        Returns:
            DocumentMetadata

        Raises:
            ValueError:
                If the document already exists.
        """

        metadata = MetadataService.extract(file_path)

        if self._repository.exists_by_hash(metadata.sha256_hash):
            raise ValueError(
                f"Document already exists: {metadata.sha256_hash}"
            )

        self._repository.create(metadata)

        self._session.commit()

        return metadata