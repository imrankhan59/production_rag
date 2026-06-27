from pathlib import Path


class VectorStore:
    """Persist and search document embeddings."""

    def __init__(self, persist_dir: Path) -> None:
        self.persist_dir = persist_dir
        self.persist_dir.mkdir(parents=True, exist_ok=True)

    def add(self, texts: list[str], embeddings: list[list[float]]) -> None:
        raise NotImplementedError("Implement vector store persistence.")

    def search(self, query_embedding: list[float], top_k: int) -> list[str]:
        raise NotImplementedError("Implement similarity search.")
