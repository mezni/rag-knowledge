import json
from pathlib import Path

from rag_knowledge.models import Document


class JSONParser:
    def parse(self, path: Path) -> Document:
        data = json.loads(path.read_text(encoding="utf-8"))

        return Document(
            id=path.stem,
            content=json.dumps(data, indent=2),
            source=str(path),
            file_type="json",
        )
