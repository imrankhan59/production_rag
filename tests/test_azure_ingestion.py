from unittest.mock import MagicMock, patch

from rag_project.config.settings import Settings
from rag_project.ingestion.azure_ingestion import ingest_from_azure_blob, save_processed_chunks


class TestAzureIngestion:
    @patch("rag_project.ingestion.azure_ingestion.load_documents_from_blob")
    def test_ingest_from_azure_blob(self, mock_load: MagicMock, tmp_path) -> None:
        from rag_project.ingestion.models import IngestedDocument

        mock_load.return_value = [
            IngestedDocument(content="abcdefghij", source="azure://documents/a.txt"),
        ]

        settings = Settings(
            data_source="azure_blob",
            azure_storage_container_name="documents",
            azure_storage_connection_string="UseDevelopmentStorage=true",
            chunk_size=4,
            chunk_overlap=2,
            processed_data_dir=tmp_path,
        )

        chunks = ingest_from_azure_blob(settings)

        assert len(chunks) == 4
        assert chunks[0].source == "azure://documents/a.txt"
        assert chunks[0].text == "abcd"

    @patch("rag_project.ingestion.azure_ingestion.load_documents_from_blob")
    def test_save_processed_chunks(self, mock_load: MagicMock, tmp_path) -> None:
        from rag_project.ingestion.models import IngestedDocument

        mock_load.return_value = [
            IngestedDocument(content="hello world", source="azure://documents/a.txt"),
        ]

        settings = Settings(
            data_source="azure_blob",
            azure_storage_container_name="documents",
            azure_storage_connection_string="UseDevelopmentStorage=true",
            chunk_size=20,
            chunk_overlap=0,
            processed_data_dir=tmp_path,
        )

        chunks = ingest_from_azure_blob(settings)
        output_path = save_processed_chunks(chunks, settings.processed_data_dir)

        assert output_path.exists()
        assert "azure_ingestion_" in output_path.name
        assert '"chunk_count": 1' in output_path.read_text(encoding="utf-8")
