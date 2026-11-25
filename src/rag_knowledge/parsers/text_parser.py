from pathlib import Path

from rag_knowledge.models import Document


class TextParser:
    def parse(self, path: Path) -> Document:
        content = path.read_text(encoding="utf-8")

        return Document(
            id=path.stem,
            content=content,
            source=str(path),
            file_type=path.suffix.lower(),
        )
