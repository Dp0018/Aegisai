---
description: Instructions for building the AegisAI Enterprise Agent Platform
globs: *
alwaysApply: true
---

<!-- BEGIN:aegisai-agent-rules -->

# This is NOT the standard stack you know

AegisAI utilizes a strict async Python architecture for the backend (FastAPI async, SQLAlchemy 2.0 async, LangGraph async workflows) and React 19 + Tailwind CSS for the Next.js frontend app. Read the relevant guidelines in the `context/` folder before writing any code.

<!-- END:aegisai-agent-rules -->

## Read Before Anything Else

Read in this exact order before any implementation:

1. context/project-overview.md
2. context/architecture.md
3. context/ui-tokens.md
4. context/ui-rules.md
5. context/ui-registry.md
6. context/code-standards.md
7. context/library-docs.md
8. context/build-plan.md
9. context/progress-tracker.md

## Rules That Never Change

- Never use hardcoded color values. Always use design tokens matching the variables in `context/ui-tokens.md`.
- Keep all Python files and frontend components under 300 lines of code.
- Update `progress-tracker.md` after every feature implementation.
- Read `context/library-docs.md` for project-specific rules before implementing any database models or LangGraph agent nodes.
- If the same problem persists after one corrective prompt, stop immediately and ask the user for advice.

## Available Skills

- `/architect` — before choosing between approaches, designing a feature/page, or making load-bearing tech decisions.
- `/develop` — to build a feature (UI or backend) from an approved design.
- `/check` — to run a code review or verify that every acceptance criterion is met.
- `/debug` — to localize and fix the root cause of an unexpected failure or bug.
- `/test` — to write Pytest suites or client-side tests after changing/creating code.
- `/scope` — to map out feature planning.
- `/sync` — to update project AGENTS.md rules after complete shifts.

## Project Backend & Credentials

This project features a custom Python + Next.js codebase.

- **Backend**: FastAPI + SQLAlchemy 2.0 (Async) + Alembic + LangGraph + PostgreSQL + Redis + Kafka.
- **Credentials**: Keys and configurations must be loaded from `.env` files in `backend/app/core/config.py`. Never hardcode secrets.
- **Key Patterns**:
  - Direct database queries must live in `app/repositories/`.
  - Business logic must live in `app/services/`.
  - Database mutations must never run inside routers (`app/api/`). Use dependency injection (`Depends`) for db sessions and services.
