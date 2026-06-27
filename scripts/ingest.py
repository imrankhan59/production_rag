"""Ingest documents from local files or Azure Blob Storage."""

from rag_project.config import get_settings
from rag_project.ingestion import (
    chunk_text,
    ingest_from_azure_blob,
    load_documents_from_path,
    save_processed_chunks,
)


def main() -> None:
    settings = get_settings()

    if settings.data_source == "azure_blob":
        chunks = ingest_from_azure_blob(settings)
        output_path = save_processed_chunks(chunks, settings.processed_data_dir)

        sources = sorted({chunk.source for chunk in chunks})
        print(f"Source: azure_blob")
        print(f"Container: {settings.azure_storage_container_name}")
        print(f"Loaded {len(sources)} blob(s), created {len(chunks)} chunk(s).")
        for source in sources:
            print(f"  - {source}")
        print(f"Saved processed chunks to: {output_path}")
        return

    documents = load_documents_from_path(settings.raw_data_dir)
    all_chunks: list[str] = []
    for document in documents:
        all_chunks.extend(
            chunk_text(
                document.content,
                chunk_size=settings.chunk_size,
                chunk_overlap=settings.chunk_overlap,
            )
        )

    print(f"Source: local")
    print(f"Loaded {len(documents)} document(s), created {len(all_chunks)} chunk(s).")
    for document in documents:
        print(f"  - {document.source}")


if __name__ == "__main__":
    main()
