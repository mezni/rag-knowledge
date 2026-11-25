import pytest

from rag_knowledge.chunking.fixed_size import (
    fixed_size_chunk,
)


def test_fixed_size_chunking():
    text = "A" * 1000

    chunks = fixed_size_chunk(
        text,
        "test-document",
        chunk_size=500,
        overlap=100,
    )

    assert len(chunks) == 3
    assert len(chunks[0].content) == 500
    assert chunks[0].id == "test-document-0000"


def test_invalid_chunk_size():
    with pytest.raises(ValueError):
        fixed_size_chunk(
            "Some text",
            "test-document",
            chunk_size=0,
        )


def test_invalid_overlap():
    with pytest.raises(ValueError):
        fixed_size_chunk(
            "Some text",
            "test-document",
            chunk_size=100,
            overlap=100,
        )
