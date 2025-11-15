# Hawker Boys TMS Operator Guide

## 1. Overview
The Hawker Boys Training Management System (TMS) supports course planning, learner management, and SkillsFuture Singapore (SSG) integrations for adult learners transitioning back to society. This guide serves operations staff, trainers, and engineers maintaining the platform.

## 2. Architecture Summary
- **Backend (FastAPI)** - Provides REST APIs, RBAC, and SSG sync jobs.
- **Database (PostgreSQL + SQLAlchemy)** - Stores core TMS data with Alembic migrations.
- **Frontend (React + Vite)** - Lightweight admin interface.
- **Background Jobs (RQ + Redis)** - Queues outbound SSG calls and retries failures.
- **Infrastructure** - Container-friendly with Docker Compose for local dev.

## 3. Platform Support
- **Local development**: macOS, Windows (WSL2), Linux.
- **Recommended hosting**:
  - *Railway*: simple deployments, managed PostgreSQL, auto HTTPS.
  - *Render*: background workers supported, Singapore data center options.
  - *AWS Lightsail*: predictable pricing, VPC peering to managed RDS if required.

### Example Deployment (Render)
1. Fork repo and connect Render account.
2. Create a PostgreSQL instance and Redis instance.
3. Add a Web Service pointing to `/backend` with `uvicorn tms.api:app --host 0.0.0.0 --port 8000`.
4. Add a Background Worker with `rq worker ssg-sync`.
5. Configure environment variables from `.env.example`.
6. Deploy frontend as static site using `npm install && npm run build`.

## 4. Developer Setup
1. Install Python 3.11+, Node.js 18+, and Redis locally.
2. Copy `.env.example` to `.env` and adjust secrets.
3. Run `make venv` to create the virtual environment.
4. Execute `make migrate` to apply migrations.
5. Launch services using `make dev` (tmux orchestrates backend, frontend, worker).
6. Run `make test` before committing.

## 5. Database & Migrations
- Alembic migrations live in `backend/tms/migrations`.
- Generate new migrations with `alembic -c backend/alembic.ini revision --autogenerate -m "describe change"`.
- Apply with `make migrate`.
- Backups: use `pg_dump -Fc <db>` nightly and test restores with `pg_restore`.

## 6. Configuration
Environment variables map to `tms.settings.Settings`.

| Variable | Description |
| --- | --- |
| `APP_NAME` | Display name for API docs. |
| `ENVIRONMENT` | `local`, `staging`, or `production`. |
| `SECRET_KEY` | JWT signing key, rotate quarterly. |
| `DATABASE_URL` | PostgreSQL DSN. |
| `REDIS_URL` | Redis connection for RQ. |
| `SSG_BASE_URL` | SSG API endpoint (sandbox or prod). |
| `SSG_CLIENT_ID` / `SSG_CLIENT_SECRET` | OAuth credentials from SSG. |
| `SSG_TIMEOUT_SECONDS` | HTTP timeout. |
| `SSG_ENV` | `sandbox` or `production` header for SSG. |
| `SSG_WEBHOOK_SECRET` | Validates inbound SSG webhooks when enabled. |
| `LOG_LEVEL` | Logging verbosity. |

## 7. Operations Guide
### Create a Course
1. Navigate to the Courses section.
2. Provide course code, name, modules, and durations.
3. Save to queue an SSG sync job.

### Create a Class Run
1. Choose an existing course.
2. Define run code, schedule, capacity, and sessions.
3. Confirm to queue SSG sync.

### Enroll Learners
1. Add learner profile (name, contact, hashed identifier for NRIC surrogate).
2. Enroll learner into class run.
3. Enrollment sync job enqueued automatically.

### Mark Attendance
1. Access attendance for a session.
2. Record status (Present, Absent, Late).
3. Sync job triggers after save.

### Trigger SSG Sync Manually
Use the Admin “Sync Now” action or run `rq enqueue tms.jobs.ssg_sync.sync_course <course_id>`.

### View Sync Status
- Monitor Redis queue via `rq info`.
- Structured logs include `ssg_request` and `ssg_error` events with correlation IDs.

### Handle Errors
Consult `/docs/SSG-Error-Catalog.md` for operator guidance. Resolve data issues locally, requeue the job, and escalate to engineering if repeated failures occur.

## 8. SSG Integration
- Obtain sandbox credentials from the [SSG Developer Portal](https://developer.ssg-wsg.gov.sg/webapp/docs/product/6kYpfJEWVb7NyYVVHvUmHi#focus).
- Populate `SSG_CLIENT_ID` and `SSG_CLIENT_SECRET` in the deployment environment.
- Test connectivity via the preflight command or `httpx` call to `/oauth/token`.
- All payload models mirror SSG sample code (see repo references in code comments).

## 9. Troubleshooting
| Symptom | Action |
| --- | --- |
| Backend fails to start | Ensure migrations applied and DB reachable. Run `make migrate`. |
| `Database connection failed` in preflight | Verify `DATABASE_URL` and network rules. |
| SSG 401/403 | Credentials expired. Rotate via SSG portal. |
| SSG 404 | Verify course or run codes exist in SSG. |
| SSG 409 | Duplicate entry - cross-check local vs SSG state. |
| SSG 422 | Payload validation failed - inspect logs for field details. |
| SSG 429 | Rate limited - wait and retry, adjust scheduling. |
| SSG 5xx | Temporary outage - retry later, queue handles automatic retries. |
| Frontend blank page | Run `npm run build` or check Vite dev server logs. |

Logs default to JSON lines. Pipe into `jq` for filtering: `tail -f backend.log | jq '.event == "ssg_error"'`.

## 10. Security & PDPA Summary
- Role-based access enforced via `X-Role` header or JWT integration.
- Sensitive identifiers stored hashed. Masked in UI by default.
- Audit trails log CRUD with actor role.
- Retention: active learner data retained 5 years post-course, archives purged annually per PDPA guidance.
- Subject access requests processed by exporting learner profile and attendance within 30 days.

## 11. Support
- Ops team: ops@hawkerboys.example
- Engineering: devs@hawkerboys.example
- Emergency escalation: call duty engineer (see internal roster).

## Dev environment
- We standardize on Node 20 via nvm
- Run `scripts/setup_node_intel.sh` once
- Run `make node_modules` to install deps
- If Terminal still cannot find node, run: `source ~/.zshrc`
