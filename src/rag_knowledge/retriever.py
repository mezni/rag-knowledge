def retrieve(
    query: str,
    documents: list[dict],
    top_k: int = 2,
) -> list[dict]:

    query_words = set(query.lower().split())

    results = []

    for document in documents:
        content_words = set(
            document["content"].lower().split()
        )

        score = len(query_words & content_words)

        if score > 0:
            results.append({
                **document,
                "score": score,
            })

    results.sort(
        key=lambda document: document["score"],
        reverse=True,
    )

    return results[:top_k]
