from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass
class DocumentMetadata:
    document_id: str
    title: str
    source: str
    file_type: str
    content_hash: str
    version: int = 1
    status: str = "processing"
    department: str | None = None
    owner: str | None = None
    access_level: str = "internal"
    tenant_id: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    extra: dict[str, Any] = field(default_factory=dict)
