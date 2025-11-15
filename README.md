# Hawker Boys Training Management System

The Hawker Boys TMS is a secure, PDPA-aware platform for managing training programmes, syncing with SkillsFuture Singapore (SSG), and supporting our culinary and financial literacy cohorts.

## Runbook

1. **Bootstrap local environment**
   - Copy `.env.example` to `.env` and adjust secrets.
   - Run `make dev` to launch PostgreSQL, Redis, the FastAPI backend, the worker, and the React admin UI.
   - Access the API docs at `http://localhost:8000/docs` and the admin UI at `http://localhost:5173`.
2. **Manage schema**
   - Use `make migrate` to generate and apply Alembic migrations.
   - Review generated files under `backend/tms/migrations/versions/` before committing.
3. **Testing**
   - Run `make test` for backend pytest and frontend lint checks.
4. **Preflight checks**
   - Run `make preflight` before deployment to validate environment variables, database connectivity, pending migrations, and Redis availability.
5. **Deployment**
   - Follow `docs/README.md` and `ops/README-deploy.md` for step-by-step guidance covering Render, Railway, and AWS Lightsail paths.

## Repository Layout

- `backend/` - FastAPI application, domain models, SSG client, and migrations.
- `frontend/` - Minimal React admin console built with Vite.
- `ops/` - Deployment artefacts including Docker Compose and platform notes.
- `docs/` - Operator documentation, ERD, security posture, and SSG error catalog.
- `static/` - Reserved for shared assets.

## Contributing

1. Create a feature branch from `main`.
2. Keep commits focused and use conventional commit messages.
3. Update documentation and tests alongside code changes.
