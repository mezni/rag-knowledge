import re

from rag_knowledge.chunking.models import Chunk


def sentence_chunk(
    text: str,
    document_id: str,
    max_sentences: int = 3,
) -> list[Chunk]:

    if max_sentences <= 0:
        raise ValueError("max_sentences must be positive")

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text.strip(),
    )

    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]

    chunks = []

    for index in range(
        0,
        len(sentences),
        max_sentences,
    ):
        content = " ".join(sentences[index : index + max_sentences])

        chunks.append(
            Chunk(
                id=f"{document_id}-{len(chunks):04d}",
                document_id=document_id,
                content=content,
                chunk_index=len(chunks),
                metadata={
                    "strategy": "sentence",
                },
            )
        )

    return chunks
