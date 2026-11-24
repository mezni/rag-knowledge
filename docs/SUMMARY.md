# Stage 7 — RAG & Knowledge Engineering

## Day 1 — RAG Fundamentals

**Day 1 of 12** · **2 hours** · **Beginner → Intermediate**

**Objective:** Understand how Retrieval-Augmented Generation (RAG) works, why it is needed, and how to build a first simple RAG pipeline using plain Python.

---

### 1. The problem RAG solves

Organizations hold large volumes of internal knowledge — HR policies, product documentation, support procedures, technical docs, contracts, and internal articles. When an employee asks a company-specific question such as "What is our company's refund policy?", a general-purpose LLM is not a reliable source:

- It does not know company-specific policies.
- Its knowledge may be outdated.
- It may hallucinate an answer.
- It cannot access internal documents on its own.

**Solution:** retrieve relevant information from company documents and supply it to the LLM as context before generating an answer. This is Retrieval-Augmented Generation (RAG).

### 2. What RAG is

RAG combines three stages:

| Stage | Responsibility |
| --- | --- |
| Retrieval | Finds relevant information |
| Augmentation | Adds retrieved information to the prompt |
| Generation | Uses an LLM to generate an answer |

The workflow: the user submits a question, the system searches the knowledge base, relevant documents are retrieved, their content is added to the LLM prompt, the LLM generates an answer grounded in that context, and the system returns the answer together with its sources.

### 3. RAG vs traditional LLM vs fine-tuning

| Approach | How it works | Best use case |
| --- | --- | --- |
| Traditional LLM | Uses pretrained knowledge | General questions |
| RAG | Retrieves external knowledge | Private and frequently changing data |
| Fine-tuning | Changes model behavior through training | Specialized behavior, style, and task patterns |

RAG and fine-tuning address different problems and can be combined.

### 4. Architecture: two separate workflows

**Indexing pipeline** — runs before users ask questions, preparing the knowledge base:

| Step | Component | Responsibility |
| --- | --- | --- |
| 1 | Documents | Original knowledge sources |
| 2 | Document Loader | Extract document content |
| 3 | Text Splitter | Divide documents into chunks |
| 4 | Embedding Model | Convert text into vectors |
| 5 | Vector Database | Store vectors and metadata |

**Query pipeline** — runs when a user asks a question:

| Step | Component | Responsibility |
| --- | --- | --- |
| 1 | User Query | Receive question |
| 2 | Query Embedding | Convert question into vector |
| 3 | Retriever | Search for relevant chunks |
| 4 | Context Builder | Prepare retrieved information |
| 5 | LLM | Generate grounded response |
| 6 | Response | Return answer and sources |

### 5. Core concepts

| Concept | Explanation |
| --- | --- |
| Document | Original knowledge source |
| Chunk | Smaller section of a document |
| Embedding | Numerical representation of text |
| Vector | Numerical array representing meaning |
| Similarity Search | Finds semantically similar vectors |
| Retriever | Component responsible for finding relevant information |
| Context Window | Maximum input the LLM can process |
| Top-K | Number of retrieved results |
| Grounding | Answering based on provided evidence |
| Hallucination | Generating unsupported or incorrect information |

**Example:** For the question "What is the refund period?", a knowledge base containing a 30-day refund policy, a support-contact note, and a refund-processing note should cause the retriever to surface the refund-period document (and possibly the processing document). The LLM then answers using only that evidence: customers can request a refund within 30 days of purchase.

### 6. Hands-on lab: first RAG pipeline

The lab builds a deliberately simplified RAG implementation with plain Python — no LangChain, LangGraph, or vector database — so the architecture is understood before advanced components are introduced.

The project is initialized with `uv`, `pytest`, and `ruff`, uses a straightforward `src`-layout package, and includes:

- Three sample policy documents (refund, shipping, support) under `data/documents/`.
- A document loader that discovers and reads every `.txt` file in a directory, returning each file's id, content, and source name.
- A basic retriever that scores documents by counting shared words between the query and document content, then returns the highest-scoring results up to `top_k`.
- A small entry point that loads the documents, runs a sample question, and prints the retrieved sources, content, and scores.
- A test module for the retriever (to be expanded in later days).

The package may need to be installed in editable mode with `uv sync` if it is not on the Python import path.

### 7. Limitations of today's implementation

The current version is intentionally basic; each limitation is addressed incrementally in later days:

| Today | Production RAG |
| --- | --- |
| Keyword matching | Semantic and hybrid search |
| Entire documents | Optimized chunks |
| No embeddings | Embedding models |
| No vector database | pgvector or Qdrant |
| No LLM | LLM integration |
| No reranking | Reranking models |
| No evaluation | Retrieval and generation evaluation |

The architecture is built up step by step rather than hidden behind a framework.

### 8. Exercises

- Explain the three stages of RAG: retrieval, augmentation, generation.
- Explain indexing vs querying: offline knowledge preparation vs runtime retrieval.
- Add a new product-policy document and verify the loader discovers it automatically.
- Change the user question and test refund, shipping, and support queries.
- Experiment with `top_k` and compare results for values 1 and 3.
- Identify three limitations of keyword retrieval: synonyms, relevance, and document size.

### 9. Git commit

`feat(rag-knowledge): initialize RAG fundamentals and basic retrieval pipeline`

### 10. What you should be able to explain after Day 1

1. What problem does RAG solve?
2. Why is RAG different from fine-tuning?
3. What is the difference between indexing and retrieval?
4. What are embeddings?
5. Why do we split documents into chunks?
6. What is a vector database?
7. Why is keyword search insufficient for advanced RAG?
8. How does retrieved context reduce hallucinations?
