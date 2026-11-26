from dataclasses import replace
from datetime import UTC, datetime

from rag_knowledge.metadata.models import DocumentMetadata
from rag_knowledge.metadata.validation import validate_metadata


class DocumentLifecycleService:
    def __init__(self):
        self.documents: dict[str, DocumentMetadata] = {}

    def register(
        self,
        metadata: DocumentMetadata,
    ) -> None:

        validate_metadata(metadata)

        key = f"{metadata.document_id}:{metadata.version}"

        if key in self.documents:
            raise ValueError("Document version already exists")

        self.documents[key] = metadata

    def activate(
        self,
        document_id: str,
        version: int,
    ) -> None:

        key = f"{document_id}:{version}"

        metadata = self.documents.get(key)

        if metadata is None:
            raise ValueError("Document version not found")

        if metadata.status != "indexed":
            raise ValueError("Only indexed documents can be activated")

        for existing_key, existing in list(self.documents.items()):
            if existing.document_id == document_id and existing.status == "active":
                self.documents[existing_key] = replace(
                    existing,
                    status="archived",
                    updated_at=datetime.now(UTC),
                )

        self.documents[key] = replace(
            metadata,
            status="active",
            updated_at=datetime.now(UTC),
        )

    def get_active(
        self,
        document_id: str,
    ) -> DocumentMetadata | None:

        for metadata in self.documents.values():
            if metadata.document_id == document_id and metadata.status == "active":
                return metadata

        return None
