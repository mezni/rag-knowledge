from rag_knowledge.chunking.sentence import sentence_chunk


def test_sentence_chunking():
    text = "First sentence. Second sentence. Third sentence. Fourth sentence."

    chunks = sentence_chunk(
        text,
        "test-document",
        max_sentences=2,
    )

    assert len(chunks) == 2
    assert "First sentence." in chunks[0].content
    assert "Fourth sentence." in chunks[1].content
