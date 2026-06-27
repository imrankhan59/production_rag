from datetime import datetime
from pathlib import Path

from rag_project.schema.document import DocumentMetadata
from rag_project.services.hash_service import HashingService


class MetadataService:
    """
    Responsible for extracting document metadata from the filesystem.

    This service does not:
    - save to the database
    - communicate with RabbitMQ
    - perform chunking
    - parse document contents
    """

    @staticmethod
    def extract(file_path: Path) -> DocumentMetadata:
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if not file_path.is_file():
            raise IsADirectoryError(f"Expected a file but got: {file_path}")

        stat = file_path.stat()

        return DocumentMetadata(
            file_name=file_path.name,
            file_path=str(file_path.resolve()),
            file_extension=file_path.suffix.lower(),
            file_size=stat.st_size,
            sha256_hash=HashingService.calculate_sha256(file_path),
            source_created_at=datetime.fromtimestamp(stat.st_ctime),
            source_modified_at=datetime.fromtimestamp(stat.st_mtime),
        )