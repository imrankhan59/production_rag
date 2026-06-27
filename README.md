# RAG Project

Retrieval-Augmented Generation (RAG) project scaffold.

## Structure

```text
rag_project/
├── src/rag_project/
│   ├── config/          # Settings and environment config
│   ├── ingestion/       # Document loading, Azure Blob, and chunking
│   ├── embeddings/      # Embedding generation
│   ├── vectorstore/     # Vector database persistence
│   ├── retrieval/       # Context retrieval
│   ├── generation/      # LLM answer generation
│   ├── pipeline/        # End-to-end RAG pipeline
│   └── cli.py           # CLI entry point
├── scripts/
│   ├── ingest.py        # Ingest documents
│   └── query.py         # Query the pipeline
├── data/
│   ├── raw/             # Source documents
│   ├── processed/       # Processed artifacts
│   └── vectorstore/     # Vector index files
├── tests/
└── notebooks/           # Experiments and exploration
```

## Setup

```bash
uv sync
cp .env.example .env
```

## Data ingestion

Ingestion supports two sources via `DATA_SOURCE`:

| Source | Env value | Required settings |
|--------|-----------|-------------------|
| Local files | `local` | Put `.txt` / `.md` files in `data/raw/` |
| Azure Blob Storage | `azure_blob` | `AZURE_STORAGE_CONTAINER_NAME` + connection string or account URL |

Supported file types: `.txt`, `.md`

### Azure Blob example

```bash
# .env
DATA_SOURCE=azure_blob
AZURE_STORAGE_CONNECTION_STRING=...
AZURE_STORAGE_CONTAINER_NAME=documents
AZURE_BLOB_PREFIX=incoming/
```

## Usage

```bash
# Run CLI
uv run rag

# Ingest documents (local or Azure Blob, based on DATA_SOURCE)
uv run python scripts/ingest.py

# Query (after wiring LLM + vector store)
uv run python scripts/query.py

# Run tests
uv run pytest
```
