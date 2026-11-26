from rag_knowledge.metadata.models import DocumentMetadata


def find_duplicate(
    content_hash: str,
    documents: list[DocumentMetadata],
) -> DocumentMetadata | None:

    for document in documents:
        if document.content_hash == content_hash:
            return document

    return None
