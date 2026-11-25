from pathlib import Path

from rag_knowledge.models import Document
from rag_knowledge.parsers.docx_parser import DOCXParser
from rag_knowledge.parsers.html_parser import HTMLParser
from rag_knowledge.parsers.json_parser import JSONParser
from rag_knowledge.parsers.pdf_parser import PDFParser
from rag_knowledge.parsers.text_parser import TextParser


class IngestionService:
    def __init__(self):
        self.parsers = {
            ".txt": TextParser(),
            ".md": TextParser(),
            ".pdf": PDFParser(),
            ".docx": DOCXParser(),
            ".html": HTMLParser(),
            ".json": JSONParser(),
        }

    def ingest(self, path: Path) -> Document:
        extension = path.suffix.lower()

        parser = self.parsers.get(extension)

        if parser is None:
            raise ValueError(f"Unsupported file format: {extension}")

        document = parser.parse(path)

        if not document.content.strip():
            raise ValueError(f"Document contains no extractable text: {path}")

        return document

    def ingest_directory(
        self,
        directory: Path,
    ) -> list[Document]:

        documents = []

        for path in directory.iterdir():
            if path.is_file():
                try:
                    documents.append(self.ingest(path))
                except (ValueError, OSError) as error:
                    print(f"Failed to ingest {path}: {error}")

        return documents
