from rag_project.embeddings.embedder import Embedder
from rag_project.vectorstore.store import VectorStore


class Retriever:
    """Retrieve relevant context for a user query."""

    def __init__(self, embedder: Embedder, vector_store: VectorStore, top_k: int) -> None:
        self.embedder = embedder
        self.vector_store = vector_store
        self.top_k = top_k

    def retrieve(self, query: str) -> list[str]:
        query_embedding = self.embedder.embed([query])[0]
        return self.vector_store.search(query_embedding, self.top_k)
