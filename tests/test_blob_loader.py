from unittest.mock import MagicMock, patch

import pytest

from rag_project.ingestion.blob_loader import load_documents_from_blob


class TestBlobLoader:
    @patch("rag_project.ingestion.blob_loader.BlobServiceClient")
    def test_load_documents_from_blob(self, mock_blob_service_client: MagicMock) -> None:
        mock_blob = MagicMock()
        mock_blob.name = "docs/readme.md"

        mock_download = MagicMock()
        mock_download.readall.return_value = b"# Hello from Azure"

        mock_blob_client = MagicMock()
        mock_blob_client.download_blob.return_value = mock_download

        mock_container_client = MagicMock()
        mock_container_client.exists.return_value = True
        mock_container_client.list_blobs.return_value = [mock_blob]
        mock_container_client.get_blob_client.return_value = mock_blob_client

        mock_service_client = MagicMock()
        mock_service_client.get_container_client.return_value = mock_container_client
        mock_blob_service_client.from_connection_string.return_value = mock_service_client

        documents = load_documents_from_blob(
            container_name="documents",
            connection_string="UseDevelopmentStorage=true",
            prefix="docs/",
        )

        assert len(documents) == 1
        assert documents[0].content == "# Hello from Azure"
        assert documents[0].source == "azure://documents/docs/readme.md"
        mock_container_client.list_blobs.assert_called_once_with(name_starts_with="docs/")

    @patch("rag_project.ingestion.blob_loader.BlobServiceClient")
    def test_load_documents_from_blob_raises_when_empty(
        self,
        mock_blob_service_client: MagicMock,
    ) -> None:
        mock_container_client = MagicMock()
        mock_container_client.exists.return_value = True
        mock_container_client.list_blobs.return_value = []

        mock_service_client = MagicMock()
        mock_service_client.get_container_client.return_value = mock_container_client
        mock_blob_service_client.from_connection_string.return_value = mock_service_client

        with pytest.raises(FileNotFoundError):
            load_documents_from_blob(
                container_name="documents",
                connection_string="UseDevelopmentStorage=true",
            )
