from pathlib import Path

from bs4 import BeautifulSoup

from rag_knowledge.models import Document


class HTMLParser:
    def parse(self, path: Path) -> Document:
        html = path.read_text(encoding="utf-8")

        soup = BeautifulSoup(html, "html.parser")

        for element in soup(["script", "style", "nav", "footer"]):
            element.decompose()

        content = soup.get_text(
            separator="\n",
            strip=True,
        )

        return Document(
            id=path.stem,
            content=content,
            source=str(path),
            file_type="html",
        )
