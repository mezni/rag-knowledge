from pathlib import Path

import pymupdf

from rag_knowledge.models import Document


class PDFParser:
    def parse(self, path: Path) -> Document:
        pages = []

        with pymupdf.open(path) as pdf:
            for page_number, page in enumerate(pdf, start=1):
                text = page.get_text("text")

                if text.strip():
                    pages.append(f"[Page {page_number}]\n{text}")

        return Document(
            id=path.stem,
            content="\n\n".join(pages),
            source=str(path),
            file_type="pdf",
            metadata={
                "page_count": len(pages),
            },
        )
