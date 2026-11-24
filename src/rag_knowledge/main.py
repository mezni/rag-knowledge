from rag_knowledge.documents import load_documents
from rag_knowledge.retriever import retrieve


def main():
    documents = load_documents("data/documents")

    query = "What is the refund period?"

    results = retrieve(query, documents)

    print(f"Question: {query}\n")

    print("Retrieved documents:")

    for document in results:
        print(f"\nSource: {document['source']}")
        print(document["content"])
        print(f"Score: {document['score']}")


if __name__ == "__main__":
    main()
