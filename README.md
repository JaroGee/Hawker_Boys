# Hawker Boys Training Management System

The Hawker Boys TMS is a PDPA-aware platform for managing courses, learners, and SkillsFuture Singapore synchronisation.

## Runbook

### Quickstart
1. Ensure Python 3.11 and Node.js 18 are installed.
2. Copy `.env.example` to `.env` and adjust values.
3. Run `make venv` then `make dev` for tmux-based orchestration.

### Scripts
- `make backend` - run FastAPI.
- `make frontend` - run Vite dev server.
- `make worker` - start RQ worker.
- `make migrate` - apply Alembic migrations.
- `make preflight` - verify environment readiness.

### Environment notes
- `.env` drives configuration via Pydantic settings.
- PostgreSQL recommended; SQLite works for local testing.

## Project Structure
Refer to `/docs/README.md` for a deep dive into architecture, PDPA controls, and SSG integration flows.
