from rag_knowledge.embeddings.sentence_transformer import (
    SentenceTransformerProvider,
)
from rag_knowledge.embeddings.similarity import (
    cosine_similarity,
)


def main():
    provider = SentenceTransformerProvider()

    documents = [
        "Customers can request a refund within 30 days.",
        "Standard shipping takes between 3 and 7 days.",
        "Customers can contact support through email.",
        "Products must be returned in their original condition.",
    ]

    query = "How long do I have to return my purchase?"

    document_embeddings = provider.embed_documents(documents)

    query_embedding = provider.embed_query(query)

    results = []

    for document, embedding in zip(
        documents,
        document_embeddings,
    ):
        score = cosine_similarity(
            query_embedding,
            embedding,
        )

        results.append((document, score))

    results.sort(
        key=lambda item: item[1],
        reverse=True,
    )

    print(f"Query: {query}\n")

    for document, score in results:
        print(f"Score: {score:.4f}")
        print(f"Document: {document}\n")


if __name__ == "__main__":
    main()
