from pathlib import Path

from sqlalchemy.orm import Session

from rag_project.observability import get_logger
from rag_project.repositories.document_repository import DocumentRepository
from rag_project.schema.document import DocumentMetadata
from rag_project.services.metadata_service import MetadataService


logger = get_logger(__name__)


class IngestionService:
    """
    Orchestrates the document ingestion workflow.
    """

    def __init__(self, session: Session) -> None:
        self._session = session
        self._repository = DocumentRepository(session)

    def ingest(self, file_path: Path) -> DocumentMetadata:
        """
        Process a document and store it if it is new.

        Duplicate documents are skipped safely.
        """

        logger.info("Starting document ingestion: %s", file_path)

        try:
            metadata = MetadataService.extract(file_path)

            logger.info(
                "Metadata extraction completed for document: %s",
                file_path,
            )

            if self._repository.exists_by_hash(metadata.sha256_hash):
                logger.info(
                    "Document already exists, skipping ingestion: %s",
                    metadata.sha256_hash,
                )
                return metadata

            self._repository.create(metadata)
            self._session.commit()

            logger.info("Document stored successfully: %s", file_path)

            return metadata

        except Exception:
            self._session.rollback()
            logger.exception("Document ingestion failed: %s", file_path)
            raise
