# Enterprise Knowledge Intelligence Platform

An AI-enhanced enterprise document intelligence platform that allows users to upload organizational documents and ask natural-language questions over their content.

The system combines document ingestion, text chunking, semantic embeddings, keyword retrieval, hybrid search, reranking, grounded answer generation, source citations, authentication, role-based access control, feedback analytics, and evaluation.

---

## 🚀 Project Overview

Organizations store critical information across HR policies, employee handbooks, SOPs, technical documentation, manuals, and internal knowledge bases.

Finding the correct information manually can be slow and error-prone.

This project provides a centralized knowledge intelligence platform where users can:

- Upload PDF documents
- Automatically extract document text
- Split documents into searchable chunks
- Generate semantic embeddings
- Search using both semantic and keyword matching
- Rerank retrieved results
- Ask natural-language questions
- Receive answers grounded in retrieved document content
- View supporting source chunks
- Submit answer feedback
- Restrict access using authentication and roles

---

## 🏗️ Architecture

```text
                    ┌──────────────────────┐
                    │     React Frontend   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    FastAPI Backend   │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
        Authentication    Document         Feedback &
           & RBAC         Ingestion        Analytics
                              │
                              ▼
                       Text Extraction
                              │
                              ▼
                           Chunking
                              │
                              ▼
                         Embeddings
                              │
                ┌─────────────┴─────────────┐
                ▼                           ▼
          Semantic Search             Keyword Search
                │                           │
                └─────────────┬─────────────┘
                              ▼
                       Hybrid Retrieval
                              │
                              ▼
                          Reranking
                              │
                              ▼
                    Grounded Answering
                              │
                              ▼
                    Grounding Validation
                              │
                              ▼
                    Answer + Citations
