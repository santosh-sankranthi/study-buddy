# The Indexing Pipeline: Load, Chunk, Embed, Store

> **Time:** ~2 min read | **Goal:** Trace the end-to-end ingestion pipeline that converts raw files into indexed, searchable chunks.

---

## 1. Anatomy of an Ingestion Pipeline

Uploading notes to a vector database is a multi-step pipeline:

```
Raw File (.md, .txt, .pdf)
         │
         ▼
[1. Document Loader]    Extract clean UTF-8 text and file metadata
         │
         ▼
[2. Chunker]            Segment into overlapping passages (e.g. 200 words)
         │
         ▼
[3. Metadata Enricher]  Attach {filename, chunk_index, subject, timestamp}
         │
         ▼
[4. Embedder]           Call embed() or embed_batch() to compute vectors
         │
         ▼
[5. Vector Store]       Persist vectors, raw text, and metadata in ChromaDB
```

---

## 2. Why Chunk-Level Metadata Matters

When an answer is generated, the student wants to know:
- *"Where did this fact come from?"*
- *"Which file and which section was it in?"*

If you don't store metadata with each chunk:
- You cannot cite sources in the UI.
- You cannot apply subject or date pre-filtering.
- You cannot update or delete specific documents when a student edits a note.

---

## 3. Atomic Indexing

In `app/main.py`, the `POST /notes/upload` endpoint processes uploads:
```python
chunks = chunk_fixed(text, chunk_size=200, overlap=50)
for idx, chunk in enumerate(chunks):
    meta = {
        "filename": filename,
        "chunk_index": idx,
        "subject": subject,
    }
    index_document(chunk, meta)
```
