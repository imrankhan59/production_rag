from rag_project.config.settings import Settings
from rag_project.ingestion.azure_ingestion import ChunkRecord, ingest_from_azure_blob
from rag_project.ingestion.blob_loader import load_documents_from_blob
from rag_project.ingestion.document_loader import load_documents_from_path
from rag_project.ingestion.models import IngestedDocument


def load_ingestion_documents(settings: Settings) -> list[IngestedDocument]:
    """Load raw documents from the configured ingestion source."""
    if settings.data_source == "azure_blob":
        if not settings.azure_storage_container_name:
            raise ValueError("AZURE_STORAGE_CONTAINER_NAME is required when DATA_SOURCE=azure_blob.")

        return load_documents_from_blob(
            container_name=settings.azure_storage_container_name,
            connection_string=settings.azure_storage_connection_string,
            account_url=settings.azure_storage_account_url,
            prefix=settings.azure_blob_prefix,
        )

    return load_documents_from_path(settings.raw_data_dir)


def run_ingestion(settings: Settings) -> tuple[list[IngestedDocument | ChunkRecord], str]:
    """Run ingestion for the configured source."""
    if settings.data_source == "azure_blob":
        return ingest_from_azure_blob(settings), "azure_blob"

    return load_documents_from_path(settings.raw_data_dir), "local"
