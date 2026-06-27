from rag_project.ingestion.chunker import chunk_text


def test_chunk_text_returns_overlapping_chunks() -> None:
    text = "abcdefghij"
    chunks = chunk_text(text, chunk_size=4, chunk_overlap=2)

    assert chunks == ["abcd", "cdef", "efgh", "ghij"]
