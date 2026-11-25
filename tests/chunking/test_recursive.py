from rag_knowledge.chunking.recursive import recursive_chunk


def test_recursive_chunking():
    text = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."

    chunks = recursive_chunk(
        text,
        "test-document",
        chunk_size=25,
    )

    assert len(chunks) > 1
    assert all(len(chunk.content) <= 25 for chunk in chunks)
