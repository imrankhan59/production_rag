from azure.core.exceptions import ResourceNotFoundError
from azure.storage.blob import BlobServiceClient

from rag_project.ingestion.document_loader import TEXT_EXTENSIONS
from rag_project.ingestion.models import IngestedDocument


def create_blob_service_client(
    *,
    connection_string: str | None,
    account_url: str | None,
) -> BlobServiceClient:
    """Create an Azure Blob service client from connection string or account URL."""
    if connection_string:
        return BlobServiceClient.from_connection_string(connection_string)

    if account_url:
        try:
            from azure.identity import DefaultAzureCredential
        except ImportError as exc:
            raise ImportError(
                "Install azure-identity to use AZURE_STORAGE_ACCOUNT_URL without a connection string."
            ) from exc

        credential = DefaultAzureCredential()
        return BlobServiceClient(account_url=account_url, credential=credential)

    raise ValueError(
        "Set AZURE_STORAGE_CONNECTION_STRING or AZURE_STORAGE_ACCOUNT_URL for blob ingestion."
    )


def load_documents_from_blob(
    *,
    container_name: str,
    connection_string: str | None = None,
    account_url: str | None = None,
    prefix: str = "",
) -> list[IngestedDocument]:
    """Download supported text documents from an Azure Blob Storage container."""
    client = create_blob_service_client(
        connection_string=connection_string,
        account_url=account_url,
    )
    container_client = client.get_container_client(container_name)

    if not container_client.exists():
        raise ResourceNotFoundError(f"Azure container not found: {container_name}")

    documents: list[IngestedDocument] = []
    for blob in container_client.list_blobs(name_starts_with=prefix or None):
        if not any(blob.name.lower().endswith(ext) for ext in TEXT_EXTENSIONS):
            continue

        blob_client = container_client.get_blob_client(blob.name)
        raw_content = blob_client.download_blob().readall()
        content = raw_content.decode("utf-8")

        documents.append(
            IngestedDocument(
                content=content,
                source=f"azure://{container_name}/{blob.name}",
            )
        )

    if not documents:
        location = f"container '{container_name}'"
        if prefix:
            location += f" with prefix '{prefix}'"
        raise FileNotFoundError(f"No supported documents found in {location}.")

    return documents
