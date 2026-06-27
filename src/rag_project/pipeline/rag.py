from rag_project.generation.llm import LLM
from rag_project.retrieval.retriever import Retriever


class RAGPipeline:
    """End-to-end retrieval-augmented generation pipeline."""

    def __init__(self, retriever: Retriever, llm: LLM) -> None:
        self.retriever = retriever
        self.llm = llm

    def query(self, question: str) -> str:
        context = self.retriever.retrieve(question)
        return self.llm.generate(question, context)
