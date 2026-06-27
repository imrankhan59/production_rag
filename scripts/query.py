"""Query the RAG pipeline."""

from rag_project.config import get_settings


def main() -> None:
    settings = get_settings()
    question = input("Ask a question: ").strip()
    if not question:
        print("No question provided.")
        return

    print(f"Query received: {question}")
    print(f"Model: {settings.llm_model}")
    print("Next: wire up Retriever + LLM in RAGPipeline.")


if __name__ == "__main__":
    main()
