# Enterprise Knowledge Intelligence Platform

A Retrieval-Augmented Generation (RAG) platform for asking natural-language questions over an organization's documents (HR policies, handbooks, SOPs, manuals) with permission-aware retrieval and source citations.

> **Current status: M0 - project scaffold only.**
> No feature is implemented yet. Nothing in this repository has been evaluated.
> This README will grow milestone by milestone; sections marked _planned_ describe intent, not existing functionality.

## Planned scope

- JWT authentication and role-based access control (ADMIN / HR / EMPLOYEE)
- PDF ingestion with page-aware extraction, chunking and metadata
- Hybrid retrieval (pgvector semantic search + PostgreSQL keyword search), reranking
- Grounded answers with citations; refusal when evidence is insufficient
- Evaluation framework (Recall@K, faithfulness, citation correctness, latency)

## Stack (decided so far)

React (Vite) - FastAPI - PostgreSQL + pgvector - Docker. Everything else is added only when a milestone needs it.

## Repository layout

See `backend/README.md`, `frontend/README.md` and `docs/`.

## Getting started

_Planned - written when M1 is verified._

## Evaluation results

Not evaluated yet.

## Limitations

To be documented honestly as the system is built.

## License

MIT - see `LICENSE`.
