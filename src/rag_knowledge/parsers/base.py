from pathlib import Path
from typing import Protocol

from rag_knowledge.models import Document


class DocumentParser(Protocol):
    def parse(self, path: Path) -> Document: ...
