# Hawker Boys Training Management System

The Hawker Boys TMS is a secure, PDPA-aware platform for managing training programmes, syncing with SkillsFuture Singapore (SSG), and supporting our culinary and financial literacy cohorts.

## Runbook

1. **Bootstrap local environment**
   - Copy `.env.example` to `.env` and adjust secrets.
   - Run `make node_env` once to install Node 20 and set up npm via nvm.
   - Run `make dev` to launch PostgreSQL, Redis, the FastAPI backend, the worker, and the React admin UI.
   - Access the API docs at `http://localhost:8000/docs` and the admin UI at `http://localhost:5173`.
2. **Manage schema**
   - Use `make migrate` to generate and apply Alembic migrations.
   - Review generated files under `backend/tms/migrations/versions/` before committing.
3. **Testing**
   - Run `make test` for backend pytest and frontend checks.
4. **Preflight checks**
   - Run `make preflight` before deployment to validate environment variables, database connectivity, pending migrations, and Redis availability.
5. **Deployment**
   - Follow `docs/README.md` and `ops/README-deploy.md` for step-by-step guidance covering Render, Railway, and AWS Lightsail paths.
6. **Portal (Next.js) development**
   - All portal source files live under `hb-portal/`.
   - Copy `hb-portal/.env.example` to `.env` and install deps with `cd hb-portal && npm install`.
   - Use the root make targets `portal-dev`, `portal-build`, `portal-start`, and `portal-seed` for common workflows.

### Helpful make targets
- `make backend` – run FastAPI locally.
- `make frontend` – run the Vite dev server.
- `make worker` – start the RQ worker.
- `make migrate` – apply Alembic migrations.
- `make preflight` – verify environment readiness.

## Streamlit admin console
- Install deps with `python3 -m pip install -r streamlit_app/requirements.txt` (use the existing venv).
- Ensure the API is running (`make dev` or `make backend`) and reachable at `http://localhost:8000/api` or set `TMS_API_URL` to another base.
- Launch the UI via `streamlit run streamlit_app/app.py` from the repo root.
- Sign in with your TMS credentials (defaults from `.env.example` are prefilled for convenience).
- The sidebar lets you adjust the API base URL if you are pointing at a remote instance.

### Environment notes
- `.env` drives configuration via Pydantic settings.
- PostgreSQL is recommended; SQLite only for quick smoke tests.

## Repository Layout
- `backend/` – FastAPI application, domain models, SSG client, and migrations.
- `frontend/` – React admin console built with Vite.
- `ops/` – Deployment artefacts including Docker Compose and platform notes.
- `docs/` – Operator documentation, ERD, security posture, and SSG error catalog.

## Contributing
1. Create a feature branch from `main`.
2. Keep commits focused and use conventional commit messages.
3. Update documentation and tests alongside code changes.
4. Refer to `/docs/README.md` for architecture, PDPA controls, and SSG integration flows.
