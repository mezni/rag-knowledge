from rag_knowledge.metadata.models import DocumentMetadata

VALID_STATUSES = {
    "processing",
    "indexed",
    "active",
    "archived",
    "failed",
}

VALID_ACCESS_LEVELS = {
    "public",
    "internal",
    "confidential",
    "restricted",
}


def validate_metadata(
    metadata: DocumentMetadata,
) -> None:

    if not metadata.document_id:
        raise ValueError("document_id is required")

    if not metadata.title:
        raise ValueError("title is required")

    if not metadata.content_hash:
        raise ValueError("content_hash is required")

    if metadata.version < 1:
        raise ValueError("version must be positive")

    if metadata.status not in VALID_STATUSES:
        raise ValueError("Invalid document status")

    if metadata.access_level not in VALID_ACCESS_LEVELS:
        raise ValueError("Invalid access level")
