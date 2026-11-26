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

---

## Day 2 — Document Ingestion Engineering

**Day 2 of 12** · **2 hours** · **Hands-on Lab**

**Objective:** Build a reusable document ingestion pipeline that can load, extract, normalize, validate, and prepare documents for downstream RAG processing. The focus is understanding how enterprise knowledge enters a RAG system.

### 1. The problem being solved

Day 1 loaded `.txt` files directly from a directory. Real enterprise knowledge is more varied: PDFs, Word documents, HTML pages, JSON files, Markdown, internal knowledge bases, and external APIs. Each format has its own structure and extraction method. A PDF, for example, may contain text paragraphs, tables, headers and footers, images, scanned pages, and metadata.

**Goal:** any supported document should enter the RAG system through a single, standardized ingestion interface that turns all formats into a common document representation.

### 2. Ingestion architecture

| Step | Component | Responsibility |
| --- | --- | --- |
| 1 | Source Discovery | Find documents |
| 2 | Document Loader | Read files |
| 3 | Parser | Extract content |
| 4 | Normalizer | Standardize extracted content |
| 5 | Metadata Extractor | Extract document metadata |
| 6 | Validator | Verify document quality |
| 7 | Document Store | Store normalized documents |

**Key distinction:** a *loader* reads the file, a *parser* understands its format and extracts its contents, and a *normalizer* standardizes the extracted information. These responsibilities must not be merged into one large function.

### 3. Document formats and dependencies

| Format | Library | Important consideration |
| --- | --- | --- |
| TXT | Python `pathlib` | Simple text extraction |
| Markdown | Python `pathlib` | Preserve headings and structure |
| PDF | PyMuPDF | Tables and scanned pages |
| DOCX | python-docx | Paragraphs and tables |
| HTML | BeautifulSoup | Remove irrelevant markup |
| JSON | Python `json` | Preserve structured data |

Dependencies are added with `uv add pymupdf python-docx beautifulsoup4`, plus `pytest` and `ruff` as dev dependencies.

### 4. Standardized document model

Every extracted document conforms to one dataclass-based model with five fields: a unique `id`, the extracted `content`, the `source` path, the `file_type`, and a `metadata` dictionary (defaulting to empty) for facts such as department, version, or page count. Downstream components consume this same model regardless of the original file format.

### 5. Parser implementations

Parsers live in a dedicated package and implement a small `DocumentParser` protocol with a single `parse(path)` method returning a `Document`. This makes the pipeline extensible: new parsers can be added without changing the ingestion code.

| Parser | Behavior |
| --- | --- |
| Text | Reads UTF-8 text; handles both `.txt` and `.md` |
| PDF | Uses PyMuPDF to extract text page by page, prefixing each page with a page marker, and records page count in metadata; text-based PDFs only (scanned pages need OCR) |
| DOCX | Uses python-docx to extract non-empty paragraphs and convert table rows into pipe-separated text |
| HTML | Uses BeautifulSoup to remove script, style, nav, and footer elements, then extracts clean text |
| JSON | Parses JSON and serializes it as indented text; for structured JSON, useful fields should be preserved as metadata rather than blindly flattening everything |

### 6. Ingestion service

A single `IngestionService` maps file extensions to parser instances (`.txt`/`.md`, `.pdf`, `.docx`, `.html`, `.json`) and exposes one `ingest(path)` entry point. It selects a parser by extension, raises an error for unsupported formats, parses the file, and rejects empty documents. This is the first reusable ingestion service; production versions will replace printed errors with structured logging, ingestion reports, retry policies, and dead-letter handling.

### 7. Testing and verification

Tests use temporary files to verify text ingestion (correct id, content, and file type), rejection of unsupported extensions, and rejection of empty documents. Verification commands: `uv run pytest` and `uv run ruff check .`.

### 8. Production ingestion challenges

| Challenge | Production solution |
| --- | --- |
| Scanned PDFs | OCR |
| Duplicate files | Content hashing |
| Corrupted files | Error handling and quarantine |
| Large documents | Streaming and batch processing |
| Changed documents | Version tracking |
| Sensitive information | Data classification and access control |
| Failed ingestion | Retry and dead-letter processing |
| Unsupported formats | Extensible parser registry |
| Poor extraction | Content-quality validation |

**Architecture decision:** keep ingestion and indexing separate. Ingestion extracts and normalizes content; indexing chunks documents, generates embeddings, and stores them. This separation allows re-indexing with a new embedding model without repeatedly parsing every source file.

---

## Day 3 — Chunking Strategies & Document Segmentation

**Day 3 of 12** · **2 hours** · **Hands-on Lab**

**Objective:** Learn how to transform large documents into smaller, meaningful, retrieval-friendly chunks while preserving context and document structure. Build a reusable chunking engine in plain Python.

### 1. The problem being solved

Day 2 built ingestion that extracts text from PDF, DOCX, HTML, JSON, and TXT files. But a company might have a 200-page refund policy, and a user asks a narrow question such as "How many days does a customer have to request a refund?" Sending the whole document to an LLM causes high token consumption, higher inference cost, irrelevant context, difficulty retrieving specific facts, context-window limits, and reduced retrieval precision.

**Solution:** divide documents into smaller pieces called chunks. The real challenge is splitting text without losing meaning.

### 2. What a chunk is

A chunk is a smaller segment of a document that can be embedded, indexed, retrieved, and passed to an LLM independently. A refund policy can be split into four chunks covering, respectively, the 30-day refund window, original-condition requirement, five-business-day processing time, and how to contact support. Each chunk becomes an independently searchable knowledge unit.

### 3. Chunking strategies

| Strategy | How it works | Advantages | Drawbacks | Best for |
| --- | --- | --- | --- | --- |
| Fixed-size | Splits by a fixed number of characters or tokens | Simple, predictable sizes, fast | Can split sentences and paragraphs, loses context | Simple documents and prototypes |
| Recursive character | Tries separators in order: paragraph, line, sentence, word, character | Preserves paragraphs where possible, natural chunks, good general purpose | Medium complexity | General document collections |
| Sentence-based | Splits on complete sentences, optionally grouping several per chunk | Preserves sentence boundaries, fewer incomplete statements | Variable sentence lengths, context between sentences may be lost | FAQs and knowledge articles |
| Semantic | Uses embeddings to split where meaning or topic changes | Meaning-oriented segmentation, better relevance | Expensive, requires embeddings and threshold tuning | Complex enterprise documentation |
| Parent-child | Stores larger parent chunks for context alongside smaller child chunks for retrieval; retrieve the child, pass its parent context to the LLM | Strong context preservation | High complexity | Long technical docs, contracts, enterprise policies |

### 4. Chunk overlap

Overlap keeps neighboring chunks sharing some text so a sentence near a boundary does not lose context. With a chunk size of 500 characters and overlap of 100, each new chunk contributes 400 characters of new text. Excessive overlap causes duplicate content, higher embedding cost, larger vector databases, and redundant retrieval results. Chunk size and overlap are tunable parameters, not universal constants.

### 5. Chunk metadata

Each chunk keeps its relationship to the original document through fields such as `chunk_id` (unique identifier), `document_id` (source document), `content`, `source` (original file), `page_number`, `chunk_index` (position in document), `parent_id` (parent chunk reference for parent-child setups), and a general `metadata` dictionary for extra attributes. This metadata becomes important later for vector databases and filtering.

### 6. Hands-on lab: chunking engine

The lab implements three strategies in plain Python — fixed-size, sentence-based, and recursive character chunking — with a `Chunk` dataclass (id, document_id, content, chunk_index, metadata) as the common representation and a dedicated `chunking` package alongside `parsers` and `ingestion`.

| Component | Behavior |
| --- | --- |
| Fixed-size | Validates positive chunk size and overlap below chunk size; steps forward by `chunk_size - overlap`; records start/end character offsets and strategy in metadata |
| Sentence-based | Splits on sentence-ending punctuation with a regex, drops empty sentences, groups up to `max_sentences` per chunk; production versions must handle abbreviations, decimals, multilingual text, and complex punctuation |
| Recursive | Tries separators from paragraphs down to characters, falls back to raw slicing; this educational version does not yet implement overlap or exact character offsets |

Unit tests cover fixed-size chunk counts, sizes and ids, invalid size and overlap errors, sentence grouping, and recursive chunk limits and count. Verification: `uv run pytest` and `uv run ruff check .`.

### 7. Strategy comparison

| Strategy | Context preservation | Complexity | Best use |
| --- | --- | --- | --- |
| Fixed-size | Low–Medium | Low | Simple text |
| Sentence-based | Medium–High | Low | FAQs |
| Recursive | High | Medium | General documents |
| Semantic | High | High | Complex knowledge |
| Parent-child | High | High | Enterprise documents |

These are general tendencies, not guaranteed retrieval-performance rankings.

### 8. Optimization trade-offs and common problems

Starting points for experiments: chunk size 300–800 tokens, overlap 10–20%, top-K 3–5 chunks, recursive strategy, metadata with source/document ID/page, and the same embedding model for documents and queries. The current Python implementations measure chunk size in **characters**, not tokens; a production system should use tokenizer-based limits because models process tokens.

| Problem | Consequence | Solution |
| --- | --- | --- |
| Chunks too small | Missing context | Increase chunk size |
| Chunks too large | Irrelevant information | Reduce chunk size |
| No overlap | Boundary information lost | Introduce overlap |
| Excessive overlap | Duplicate retrieval | Reduce overlap |
| Broken tables | Lost relationships | Structure-aware parsing |
| Lost headings | Ambiguous chunks | Preserve document hierarchy |

### 9. Production architecture evolution

The pipeline now has three distinct stages: **source documents → document ingestion → normalized documents → chunking engine → chunk validation → chunk metadata → ready for embeddings**. Embeddings and vector storage have not been implemented yet; that is the next stage.

---

## Day 4 — Metadata Engineering & Document Lifecycle Management

**Day 4 of 12** · **2 hours** · **Hands-on Lab**

**Objective:** Build a reliable metadata and document lifecycle management system that tracks document identity, ownership, versions, updates, duplicates, and relationships between documents and chunks.

### 1. The problem being solved

In an enterprise RAG system with 100,000 documents, a refund policy may be updated from "refunds within 30 days" to "refunds within 45 days" while the old version remains indexed. An employee asking "What is the current refund period?" then receives outdated information. Related problems: duplicate documents, missing ownership, no version history, no way to trace a chunk to its document, no department filtering, and unauthorized retrieval of confidential content.

**Solution:** implement document metadata management and lifecycle tracking.

### 2. Document metadata

Metadata is structured information *describing* a document (identity, title, source, department, version, status, timestamps, access level), not its actual content. It enables filtering, tracking, governance, and retrieval.

| Category | Examples | Purpose |
| --- | --- | --- |
| Identity | `document_id`, `source` | Identify documents |
| Descriptive | `title`, `description` | Understand content |
| Organizational | `department`, `owner` | Business classification |
| Temporal | `created_at`, `updated_at` | Track changes |
| Versioning | `version`, `content_hash` | Track revisions |
| Security | `access_level`, `tenant_id` | Control access |
| Technical | `file_type`, `file_size` | Processing information |
| Retrieval | `page_number`, `chunk_index` | Source traceability |

Timestamps use UTC (`datetime.now(timezone.utc)`) to avoid inconsistency across distributed systems.

### 3. Document lifecycle

| Stage | Description |
| --- | --- |
| Uploaded | Document received |
| Processing | Extracted and normalized |
| Validated | Content and metadata validated |
| Indexed | Chunks and embeddings stored |
| Active | Available for retrieval |
| Updated | New version received |
| Archived | No longer active |
| Deleted | Removed per retention policy |

A document must not become searchable until ingestion and indexing succeed.

### 4. Identity and duplicate detection

**Document identity** (which logical business document) and **content identity** (identical file bytes) are distinct. SHA-256 hashes of file bytes detect exact duplicates with extremely high confidence, but cannot detect semantic duplicates — files with different formatting but the same information.

### 5. Version management

Keep a stable logical document ID, give each revision its own version, preserve its content hash, maintain publication and effective dates, never mix chunks from different versions, and block archived versions from normal retrieval. For the refund-policy example, version 1 (30 days) is archived and version 2 (45 days) is active — history is preserved while retrieval uses only the active version.

### 6. Chunk traceability

Every chunk records its `document_id`, `version_id`, `chunk_index`, and metadata (department, source, page number, status). This enables source citations, document-level filtering, version-specific retrieval, document deletion, and audit trails.

### 7. Hands-on lab: metadata and lifecycle management

The lab extends the Python project with a `metadata` package (`models.py`, `hashing.py`, `validation.py`, `duplicate_detection.py`), a `lifecycle/service.py`, and matching tests.

| Component | Behavior |
| --- | --- |
| `DocumentMetadata` | Dataclass with identity, file type, content hash, version (default 1), status (default `processing`), optional department/owner/tenant, UTC timestamps, and an `extra` dict |
| Hashing | `calculate_content_hash` hashes original bytes; `calculate_text_hash` hashes stripped UTF-8 text |
| Validation | Requires document id, title, content hash, and positive version; validates status (`processing`, `indexed`, `active`, `archived`, `failed`) and access level (`public`, `internal`, `confidential`, `restricted`) |
| `DocumentLifecycleService` | In-memory store keyed by `document_id:version`; `register` validates and rejects duplicate versions; `activate` promotes an indexed version and archives the previous version |
| Duplicate detection | `find_duplicate` scans a list for a matching content hash; production uses a database index instead |

Activation and archival must be atomic in persistent storage in production, with a constraint allowing only one active version per logical document. Verification: `uv run pytest` and `uv run ruff check .`.

### 8. Production lifecycle architecture

**Document Uploaded → Calculate Content Hash → Duplicate? (yes: skip or link existing; no: continue) → Extract and Normalize → Validate Metadata → Chunk Document → Generate Embeddings → Store Chunks and Vectors → Validate Indexing → Activate New Version → Archive Previous Version.** The new version is activated only after indexing succeeds.

### 9. Enterprise design considerations

| Concern | Design approach |
| --- | --- |
| Duplicate files | SHA-256 content hashes |
| Document updates | Version management |
| Outdated content | Active-version filtering |
| Source traceability | Document and chunk IDs |
| Tenant isolation | Tenant metadata and database enforcement |
| Confidentiality | Authorization-aware retrieval |
| Document deletion | Cascading index cleanup |
| Auditability | Lifecycle event history |

**Critical security point:** metadata filtering is not authorization. Access control must be enforced by trusted server-side identity and authorization logic before chunks are returned.
