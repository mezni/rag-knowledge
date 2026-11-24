from pathlib import Path


def load_documents(directory: str) -> list[dict]:
    documents = []

    for file_path in Path(directory).glob("*.txt"):
        content = file_path.read_text(encoding="utf-8")

        documents.append({
            "id": file_path.stem,
            "content": content,
            "source": file_path.name,
        })

    return documents
