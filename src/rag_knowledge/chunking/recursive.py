from rag_knowledge.chunking.models import Chunk

SEPARATORS = ["\n\n", "\n", ". ", " ", ""]


def recursive_split(
    text: str,
    chunk_size: int,
    separators: list[str] | None = None,
) -> list[str]:

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    separators = separators or SEPARATORS

    if len(text) <= chunk_size:
        return [text] if text else []

    separator = next(
        (item for item in separators if item and item in text),
        "",
    )

    if not separator:
        return [
            text[index : index + chunk_size]
            for index in range(0, len(text), chunk_size)
        ]

    parts = text.split(separator)

    chunks = []
    current = ""

    for part in parts:
        candidate = f"{current}{separator}{part}" if current else part

        if len(candidate) <= chunk_size:
            current = candidate
        else:
            if current:
                chunks.extend(
                    recursive_split(
                        current,
                        chunk_size,
                        separators[separators.index(separator) + 1 :],
                    )
                )

            current = part

    if current:
        chunks.extend(
            recursive_split(
                current,
                chunk_size,
                separators[separators.index(separator) + 1 :],
            )
        )

    return chunks


def recursive_chunk(
    text: str,
    document_id: str,
    chunk_size: int = 500,
) -> list[Chunk]:

    contents = recursive_split(text, chunk_size)

    return [
        Chunk(
            id=f"{document_id}-{index:04d}",
            document_id=document_id,
            content=content,
            chunk_index=index,
            metadata={
                "strategy": "recursive",
            },
        )
        for index, content in enumerate(contents)
    ]
