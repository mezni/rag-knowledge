from rag_knowledge.metadata.hashing import (
    calculate_content_hash,
)


def test_same_content_has_same_hash():
    first = calculate_content_hash(b"refund policy")
    second = calculate_content_hash(b"refund policy")

    assert first == second


def test_different_content_has_different_hash():
    first = calculate_content_hash(b"refund policy")
    second = calculate_content_hash(b"shipping policy")

    assert first != second
