import pytest

from rag_knowledge.lifecycle.service import (
    DocumentLifecycleService,
)
from rag_knowledge.metadata.models import DocumentMetadata


def make_document(version: int, status: str):
    return DocumentMetadata(
        document_id="refund-policy",
        title="Refund Policy",
        source="refund-policy.pdf",
        file_type="pdf",
        content_hash=f"hash-{version}",
        version=version,
        status=status,
    )


def test_activate_indexed_document():
    service = DocumentLifecycleService()

    service.register(make_document(1, "indexed"))
    service.activate("refund-policy", 1)

    active = service.get_active("refund-policy")

    assert active is not None
    assert active.version == 1
    assert active.status == "active"


def test_new_version_archives_previous_version():
    service = DocumentLifecycleService()

    service.register(make_document(1, "indexed"))
    service.activate("refund-policy", 1)

    service.register(make_document(2, "indexed"))
    service.activate("refund-policy", 2)

    active = service.get_active("refund-policy")

    assert active.version == 2

    old = service.documents["refund-policy:1"]

    assert old.status == "archived"


def test_cannot_activate_unindexed_document():
    service = DocumentLifecycleService()

    service.register(make_document(1, "processing"))

    with pytest.raises(ValueError):
        service.activate("refund-policy", 1)
