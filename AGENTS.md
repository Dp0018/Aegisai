# AegisAI Enterprise Agent Platform - Project Guidelines

This file outlines the development rules, technology stack, directory layout, and architectural decisions for AegisAI. All agents working on this project must adhere strictly to these rules.

## Tech Stack

### Backend
* **Language & Runtime**: Python 3.11
* **Web Framework**: FastAPI (Async)
* **Agent Framework**: LangGraph + LangChain
* **Database & ORM**: PostgreSQL + SQLAlchemy 2.0 (Async) + Alembic
* **Vector DB**: ChromaDB
* **Caching & Revocation**: Redis (Async)
* **Message Broker**: Kafka

### Frontend
* **Framework**: Next.js (App Router, React 19, TypeScript)
* **Styling**: Tailwind CSS
* **Data Fetching**: TanStack Query
* **Forms & Validation**: React Hook Form + Zod

## Directory Layout (Option A - Split)

```text
/aegisai
  ├── backend/
  │    ├── app/
  │    │    ├── api/           # Route handlers and endpoints
  │    │    ├── core/          # App configurations, secrets, and dependencies
  │    │    ├── db/            # Connection engine & session generators
  │    │    ├── models/        # SQLAlchemy tables (User, AuditLog, etc.)
  │    │    ├── schemas/       # Pydantic validation schemas
  │    │    ├── repositories/  # Database access interfaces
  │    │    ├── services/      # Business logic controllers
  │    │    ├── agents/        # LangGraph definitions
  │    │    └── tools/         # Executor tools
  │    ├── tests/              # Pytest modules
  │    └── requirements.txt    # Python dependency file
  ├── frontend/                # Next.js client application
  ├── docker-compose.yml       # PostgreSQL and Redis setup
  └── AGENTS.md                # System instructions (this file)
```

## Development Rules & Coding Standards

1. **Feature-by-Feature Development**: Never generate entire features or multiple files without step-by-step review and direct user instructions. Build incrementally.
2. **Keep Modules Under 300 Lines**: To preserve maintainability and readability, files must not exceed 300 lines whenever possible.
3. **Clean Architecture**: Decouple layers cleanly. 
   * Database models live in `models/`.
   * Pydantic schemas for request validation live in `schemas/`.
   * Direct DB queries live in `repositories/`.
   * Business logic live in `services/`.
   * Controllers/Endpoints live in `api/` and must never run direct DB mutations.
4. **Dependency Injection**: Utilize FastAPI's dependency injection (`Depends`) for services, databases, cache access, and RBAC security checkers.
5. **No Mock Implementations**: Avoid mock responses unless requested by the user. Connect real databases and utilities where possible.
6. **SQLAlchemy 2.0 Syntax**: Always use the modern `select()` and async SQLAlchemy session mappings. Avoid obsolete 1.x syntax.
