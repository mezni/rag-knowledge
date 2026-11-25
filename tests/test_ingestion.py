from pathlib import Path

import pytest

from rag_knowledge.ingestion import IngestionService


def test_ingest_text_document(tmp_path: Path):
    file_path = tmp_path / "policy.txt"

    file_path.write_text(
        "Refunds are available within 30 days.",
        encoding="utf-8",
    )

    service = IngestionService()

    document = service.ingest(file_path)

    assert document.id == "policy"
    assert "30 days" in document.content
    assert document.file_type == ".txt"


def test_unsupported_file(tmp_path: Path):
    file_path = tmp_path / "policy.xyz"
    file_path.write_text("content")

    service = IngestionService()

    with pytest.raises(ValueError):
        service.ingest(file_path)


def test_empty_document(tmp_path: Path):
    file_path = tmp_path / "empty.txt"
    file_path.write_text("   ")

    service = IngestionService()

    with pytest.raises(ValueError):
        service.ingest(file_path)
