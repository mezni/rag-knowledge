from pathlib import Path

from docx import Document as WordDocument

from rag_knowledge.models import Document


class DOCXParser:
    def parse(self, path: Path) -> Document:
        word_doc = WordDocument(path)

        paragraphs = [
            paragraph.text
            for paragraph in word_doc.paragraphs
            if paragraph.text.strip()
        ]

        tables = []

        for table in word_doc.tables:
            for row in table.rows:
                tables.append(" | ".join(cell.text for cell in row.cells))

        content = "\n".join(paragraphs + tables)

        return Document(
            id=path.stem,
            content=content,
            source=str(path),
            file_type="docx",
        )
