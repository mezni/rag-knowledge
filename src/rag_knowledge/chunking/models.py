from dataclasses import dataclass, field
from typing import Any


@dataclass
class Chunk:
    id: str
    document_id: str
    content: str
    chunk_index: int
    metadata: dict[str, Any] = field(default_factory=dict)
