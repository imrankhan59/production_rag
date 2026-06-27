from pathlib import Path

from rag_project.ingestion.models import IngestedDocument

TEXT_EXTENSIONS = {".txt", ".md"}


def load_documents_from_path(path: Path) -> list[IngestedDocument]:
    """Load text documents from a local file or directory."""
    if path.is_file():
        if path.suffix.lower() not in TEXT_EXTENSIONS:
            raise ValueError(f"Unsupported file type: {path.suffix}")
        return [IngestedDocument(content=path.read_text(encoding="utf-8"), source=str(path))]

    if path.is_dir():
        documents: list[IngestedDocument] = []
        for file_path in sorted(path.glob("**/*")):
            if file_path.is_file() and file_path.suffix.lower() in TEXT_EXTENSIONS:
                documents.append(
                    IngestedDocument(
                        content=file_path.read_text(encoding="utf-8"),
                        source=str(file_path),
                    )
                )
        if documents:
            return documents

    raise FileNotFoundError(f"No documents found at: {path}")
