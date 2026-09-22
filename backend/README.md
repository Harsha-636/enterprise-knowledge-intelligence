# Backend

FastAPI modular monolith. Status: **M0 - structure only, nothing implemented.**

| Package | Responsibility (built in milestone) |
|---|---|
| `app/api` | HTTP routers only; no business logic (M1+) |
| `app/auth` | JWT creation/verification, password hashing, current-user dependencies (M3) |
| `app/database` | Engine, sessions, migrations glue (M2) |
| `app/models` | SQLAlchemy ORM tables (M2) |
| `app/schemas` | Pydantic request/response models (M1+) |
| `app/services` | Business logic that orchestrates the other packages (M3+) |
| `app/ingestion` | Validate -> extract -> clean -> chunk -> embed pipeline (M4-M6) |
| `app/retrieval` | Vector, keyword, hybrid search, reranking, permission filtering (M7, M10, M11, M14) |
| `app/generation` | Prompt templates, LLM client, grounding validator (M8, M17) |
| `app/security` | Prompt-injection checks, file validation, audit helpers (M16) |
| `app/evaluation` | Metrics and evaluation runner (M19) |
| `app/utils` | Logging, config helpers (M1) |
