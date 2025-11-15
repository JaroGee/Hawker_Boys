# Hawker Boys TMS Operator Guide

## 1. Overview
The Hawker Boys Training Management System (TMS) supports our post-release learners with secure course administration, SSG grant eligibility workflows, and operational guardrails designed for a small but vigilant team. This guide is written for operations staff, trainers, and volunteer engineers who keep the platform running.

## 2. Architecture Summary
- **Backend**: FastAPI service with SQLAlchemy ORM, Alembic migrations, and JWT-based RBAC.
- **Database**: PostgreSQL with encrypted volumes recommended at the platform layer.
- **Background Jobs**: RQ workers connected to Redis queue outbound SSG updates so classroom activities continue if SSG is down.
- **Frontend**: Lightweight React + Vite admin console for quick operator actions.
- **SSG Integration**: Typed HTTPX client with exponential backoff, aligned with official sample codes (see inline references in `backend/tms/ssg_client`).
- **Observability**: Structured logging via Loguru, optional Sentry integration through `SENTRY_DSN`.

## 3. Supported Platforms
- **Local development**: macOS (Apple Silicon), Windows 11 (WSL2), and Ubuntu 22.04.
- **Recommended hosted options**:
  1. **Railway** - fastest setup, managed Postgres and Redis, supports secrets UI.
  2. **Render** - predictable pricing, native background worker support.
  3. **AWS Lightsail** - for teams already on AWS, provides Singapore region instances with fixed monthly cost.

## 4. Quick Deployment (Render example)
1. Fork the repository or connect Render to the GitHub repo.
2. Provision Render PostgreSQL (small) and Redis (starter) instances.
3. Create a Web Service:
   - Build command: `cd backend && pip install . && alembic upgrade head`
   - Start command: `uvicorn tms.main:app --host 0.0.0.0 --port 8000`
   - Add environment variables from `.env.example`.
4. Create a Background Worker using the same image with command `rq worker ssg_sync`.
5. Deploy the frontend as a Static Site using `frontend` folder with build command `npm install && npm run build` and publish directory `frontend/dist`.
6. Configure health checks at `/healthz` (liveness) and `/readiness` (readiness).

## 5. Developer Setup
1. **Clone and environment**
   ```bash
   git clone git@github.com:JaroGee/Hawker_Boys.git
   cd Hawker_Boys
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e backend/.[dev]
   corepack enable
   cd frontend && npm install && cd ..
   ```
2. **Environment variables**
   - Copy `.env.example` to `.env`.
   - Update secrets (use a password manager to store originals).
3. **Database migrations**
   ```bash
   make migrate
   ```
4. **Run services**
   ```bash
   make dev
   ```
   - Backend API: `http://localhost:8000`
   - Swagger UI: `http://localhost:8000/docs`
   - Frontend admin: `http://localhost:5173`
   - RQ worker logs appear in the console.
5. **Testing**
   ```bash
   make test
   ```

## 6. Configuration Reference
| Variable | Purpose | Example |
| --- | --- | --- |
| `APP_ENV` | Runtime environment label | `local` |
| `API_HOST` / `API_PORT` | Bind address for FastAPI | `0.0.0.0` / `8000` |
| `SECRET_KEY` | JWT signing key (generate via `openssl rand -hex 32`) | `hexstring` |
| `DATABASE_URL` | SQLAlchemy connection string | `postgresql+psycopg://user:pass@host/db` |
| `REDIS_URL` | Redis instance for RQ | `redis://localhost:6379/0` |
| `SSG_BASE_URL` | SSG API base | `https://sandbox-developer.ssg-wsg.gov.sg/api` |
| `SSG_CLIENT_ID` / `SSG_CLIENT_SECRET` | OAuth client credentials from SSG | `xxxx` |
| `SSG_TIMEOUT_SECONDS` | HTTP timeout in seconds | `30` |
| `SSG_ENV` | `sandbox` or `prod` | `sandbox` |
| `SSG_WEBHOOK_SECRET` | Signature validation key (if webhooks enabled) | `generated-string` |
| `DEFAULT_ADMIN_EMAIL` / `DEFAULT_ADMIN_PASSWORD` | Bootstrapped admin login | `ops@example.org` / `ChangeMe123!` |
| `SENTRY_DSN` | Optional error tracking | `https://key@o.sentry.io/project` |

## 7. Operations Guide
### 7.1 Create a Course and Class Run
1. Sign in using the admin UI with the default admin credentials (change immediately).
2. Create a course via API or UI (UI integration planned) with modules defined.
3. Add class runs with start/end dates and reference code.
4. Confirm that the SSG sync job is queued (see worker logs or `/api/v1/audit`).

### 7.2 Enroll Learners
1. Register the learner record with masked NRIC (mask example: `S1234567*`).
2. Enroll the learner into the class run via API `/api/v1/enrollments`.
3. Verify audit log entry and pending SSG sync job.

### 7.3 Mark Attendance
1. After each session, trainers submit attendance via `/api/v1/attendance`.
2. Attendance records automatically trigger SSG submission jobs.
3. Monitor job success under **SSG Sync Status** in the frontend.

### 7.4 Trigger SSG Sync
- Syncs occur automatically when records are created/updated.
- To retry manually, enqueue via RQ dashboard or rerun the relevant job function, e.g. `enqueue_ssg_sync("tms.jobs.ssg.sync_course_to_ssg", course_id)`.

### 7.5 Review Sync Status and Resolve Errors
- Inspect `/api/v1/audit` for audit trail and `/logs` (application logs) for SSG correlation IDs.
- Cross-reference the response code with `docs/SSG-Error-Catalog.md` for corrective steps.
- If repeated failures occur, pause retries, validate payloads, and escalate to SSG support with correlation IDs.

## 8. SSG Integration Checklist
1. Request sandbox credentials from SSG Developer Portal under the Training Provider product.
2. Populate `.env` with `SSG_CLIENT_ID`, `SSG_CLIENT_SECRET`, and `SSG_WEBHOOK_SECRET`.
3. Run `make preflight` to confirm credentials and connectivity.
4. Test a harmless GET request using `python -m httpx https://.../ping` or the provided `/api/v1/ssg/test` endpoint (future enhancement).
5. Review SSG sample code references (see inline comments referencing `ssg-wsg/Sample-Codes`).

## 9. Troubleshooting
| Symptom | Suggested Fix |
| --- | --- |
| API fails to start | Run `make preflight`; confirm Postgres and Redis containers are up. Check `.env` formatting. |
| DB connection errors | Ensure `DATABASE_URL` points to reachable host and that migrations ran (`alembic upgrade head`). |
| SSG 401/403 | Credentials invalid or expired. Rotate via SSG portal and update secrets. |
| SSG 404 | Verify course/run IDs exist in SSG; ensure payload references correct keys. |
| SSG 409 | Duplicate submission; check idempotency keys and audit logs for earlier success. |
| SSG 422 | Payload validation failed. Compare against SSG schema and sanitize data (see error catalog). |
| SSG 429 | Too many requests. Allow the retry policy to back off; avoid manual rapid retries. |
| SSG 5xx | SSG outage. Jobs will retry automatically; inform staff and continue offline tracking. |
| Frontend build fails | Delete `frontend/node_modules`, rerun `npm install`. |

Logs are written to stdout and should be captured by hosting platform. Include correlation IDs when escalating issues.

## 10. Security and PDPA Summary
- JWT-based RBAC enforces least privilege for Admin, Ops, Trainer, Learner roles.
- NRIC fields are masked at entry; full NRICs should not be stored.
- Audit trails capture create/update/delete/access on sensitive entities.
- Data retention policy suggestions are in `docs/SECURITY-PDPA.md`.
- Encrypted connections are mandatory (HTTPS in front of the API). Engage PDPA-aware legal counsel before production rollout.

## 11. Support Contacts
- **Operations Lead**: ops@hawkerboys.sg
- **Engineering Volunteers**: dev@hawkerboys.sg
- **Escalation**: call the Duty Manager when PDPA incidents are suspected.
