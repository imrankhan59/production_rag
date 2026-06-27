from sqlalchemy import select
from sqlalchemy.orm import Session

from rag_project.database.models import Document
from rag_project.schema.document import DocumentMetadata


class DocumentRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, document: DocumentMetadata) -> Document:
        db_document = Document(
            file_name=document.file_name,
            file_path=document.file_path,
            file_extension=document.file_extension,
            file_size=document.file_size,
            sha256_hash=document.sha256_hash,
            source_created_at=document.source_created_at,
            source_modified_at=document.source_modified_at,
        )

        self._session.add(db_document)
        self._session.flush()
        self._session.refresh(db_document)

        return db_document

    def get_by_id(self, document_id: int) -> Document | None:
        statement = select(Document).where(Document.id == document_id)

        return self._session.scalar(statement)

    def get_by_hash(self, sha256_hash: str) -> Document | None:
        statement = (
            select(Document)
            .where(Document.sha256_hash == sha256_hash)
        )

        return self._session.scalar(statement)

    def exists_by_hash(self, sha256_hash: str) -> bool:
        statement = (
            select(Document.id)
            .where(Document.sha256_hash == sha256_hash)
            .limit(1)
        )

        return self._session.scalar(statement) is not None

    def update(self, document: Document) -> Document:
        db_document = self._session.merge(document)
        self._session.flush()
        self._session.refresh(db_document)

        return db_document

    def delete(self, document: Document) -> None:
        self._session.delete(document)
        self._session.flush()