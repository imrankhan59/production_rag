class Embedder:
    """Generate vector embeddings for text chunks."""

    def __init__(self, model: str) -> None:
        self.model = model

    def embed(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError(
            "Implement embedding logic (e.g. OpenAI, sentence-transformers)."
        )
