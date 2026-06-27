import os
from pathlib import Path

from rag_project.config.settings import Settings
from rag_project.ingestion.blob_loader import load_documents_from_blob


def ingest_from_azure_blob(settings: Settings, output_dir: Path) -> list[Path]:
    """
    Download documents from Azure Blob Storage and save them locally.
    No chunking, no processing — just raw ingestion.
    """

    if not settings.azure_storage_container_name:
        raise ValueError("AZURE_STORAGE_CONTAINER_NAME is required.")

    # Load raw files from blob
    documents = load_documents_from_blob(
        container_name=settings.azure_storage_container_name,
        connection_string=settings.azure_storage_connection_string,
        account_url=settings.azure_storage_account_url,
        prefix=settings.azure_blob_prefix,
    )

    output_dir.mkdir(parents=True, exist_ok=True)

    saved_files: list[Path] = []

    for doc in documents:
        # Keep original filename if available, otherwise fallback
        filename = os.path.basename(doc.source)
        if not filename:
            filename = f"file_{len(saved_files)}.bin"

        file_path = output_dir / filename

        # Save raw content
        if isinstance(doc.content, bytes):
            file_path.write_bytes(doc.content)
        else:
            file_path.write_text(doc.content, encoding="utf-8")

        saved_files.append(file_path)

    return saved_files
