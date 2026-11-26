import hashlib


def calculate_content_hash(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def calculate_text_hash(content: str) -> str:
    normalized = content.strip()

    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()
