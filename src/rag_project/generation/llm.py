class LLM:
    """Generate answers from a prompt and retrieved context."""

    def __init__(self, model: str, api_key: str | None = None) -> None:
        self.model = model
        self.api_key = api_key

    def generate(self, query: str, context: list[str]) -> str:
        raise NotImplementedError("Implement LLM generation logic.")
