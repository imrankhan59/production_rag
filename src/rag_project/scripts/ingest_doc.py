from pathlib import Path

from rag_project.database.connection import get_session
from rag_project.services.ingestion_service import IngestionService


def main() -> None:
    file_path = Path("data/raw/AAMHRPOLICYMANUAL-English.pdf")

    with get_session() as session:
        ingestion_service = IngestionService(session)
        metadata = ingestion_service.ingest(file_path)

    print(metadata.model_dump())


if __name__ == "__main__":
    main()