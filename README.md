# Enterprise Knowledge Intelligence Platform

An enterprise document intelligence and Retrieval-Augmented Generation (RAG) platform for uploading organizational PDFs, searching their content, and answering natural-language questions using retrieved document evidence.

## Project Overview

Organizations store important knowledge across HR policies, employee handbooks, SOPs, technical documentation, manuals, and internal guides.

This project provides a centralized knowledge intelligence platform where users can:

- Upload PDF documents
- Extract text automatically
- Split documents into searchable chunks
- Generate semantic embeddings
- Search using semantic and keyword retrieval
- Combine retrieval signals using hybrid search
- Rerank retrieved results
- Ask natural-language questions
- Receive answers based on retrieved document content
- View supporting source chunks and retrieval scores
- Submit answer feedback
- Use authenticated and role-protected APIs
- Evaluate retrieval performance using a test dataset

---

## Key Features

### Document Intelligence

- PDF document upload
- Automatic text extraction using `pypdf`
- Document metadata extraction
- Word and character statistics
- Overlapping text chunking
- Document ownership tracking

### Retrieval-Augmented Search

The retrieval pipeline combines multiple techniques:

1. Query rewriting
2. Semantic embedding generation
3. Semantic similarity search
4. Keyword retrieval
5. Hybrid scoring
6. Cross-encoder reranking
7. Context assembly
8. Answer extraction
9. Grounding validation
10. Source evidence presentation

### Authentication and Security

- JWT-based authentication
- Argon2 password hashing
- Protected API endpoints
- Admin-only endpoints
- User-level document isolation
- Environment-based secret configuration
- Passwords are never stored as plaintext

### Feedback and Analytics

Users can mark generated answers as:

- Helpful
- Not helpful

Administrators can view:

- Total feedback
- Helpful responses
- Not-helpful responses
- Average grounding score

### Evaluation

The project includes a retrieval evaluation dataset and evaluation script for measuring expected keyword coverage in retrieved document context.

---

## System Architecture

```text
                    React Frontend
                          |
                          v
                   FastAPI Backend
                          |
          +---------------+---------------+
          |               |               |
          v               v               v
   Authentication    Document          Feedback
       & RBAC         Ingestion        & Analytics
                          |
                          v
                   PDF Text Extraction
                          |
                          v
                       Chunking
                          |
                          v
                      Embeddings
                          |
              +-----------+-----------+
              |                       |
              v                       v
       Semantic Search         Keyword Search
              |                       |
              +-----------+-----------+
                          |
                          v
                   Hybrid Retrieval
                          |
                          v
                    Cross-Encoder
                      Reranking
                          |
                          v
                  Context Assembly
                          |
                          v
              Extractive Answer Pipeline
                          |
                          v
                Grounding Validation
                          |
                          v
              Answer + Source Chunks
