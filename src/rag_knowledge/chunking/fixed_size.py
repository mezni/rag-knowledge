from rag_knowledge.chunking.models import Chunk


def fixed_size_chunk(
    text: str,
    document_id: str,
    chunk_size: int = 500,
    overlap: int = 100,
) -> list[Chunk]:

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and < chunk_size")

    chunks = []
    start = 0
    index = 0
    step = chunk_size - overlap

    while start < len(text):
        content = text[start : start + chunk_size]

        chunks.append(
            Chunk(
                id=f"{document_id}-{index:04d}",
                document_id=document_id,
                content=content,
                chunk_index=index,
                metadata={
                    "start_char": start,
                    "end_char": start + len(content),
                    "strategy": "fixed_size",
                },
            )
        )

        start += step
        index += 1

    return chunks
