import pytest

from rag_knowledge.embeddings.sentence_transformer import (
    SentenceTransformerProvider,
)


@pytest.fixture(scope="module")
def provider():
    return SentenceTransformerProvider()


def test_document_embedding_dimensions(provider):
    embeddings = provider.embed_documents(
        [
            "Refund policy",
            "Shipping policy",
        ]
    )

    assert len(embeddings) == 2
    assert all(len(vector) == 384 for vector in embeddings)


def test_query_embedding_dimensions(provider):
    embedding = provider.embed_query("How can I get a refund?")

    assert len(embedding) == 384


def test_empty_query(provider):
    with pytest.raises(ValueError):
        provider.embed_query("   ")
