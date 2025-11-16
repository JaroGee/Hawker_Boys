# Render Deployment Guide

The stack ships as three Render services (API, worker, and static frontend) plus managed Postgres and Redis. Complete the following steps to get a smoke deployment in under 30 minutes.

## 1. Prepare configuration

1. Copy `.env.example` to `.env` and populate **all** required values (secrets, SSG credentials, `FRONTEND_ORIGIN`, etc.).
2. Run `make preflight && make test` locally. Fix any failures before deploying.
3. Build the production bundles once (optional sanity check):
   ```bash
   docker compose -f ops/docker-compose.yml up --build api worker frontend db redis
   ```

## 2. Provision managed services on Render

1. **Managed Postgres**: PostgreSQL 15 in the Singapore region. Note the internal database URL and set it later as `DATABASE_URL`.
2. **Managed Redis**: Redis 7 instance. Capture the Redis URL for `REDIS_URL`.

## 3. Backend Web Service

| Setting | Value |
| --- | --- |
| Runtime | Docker |
| Start command | `uvicorn tms.main:app --host 0.0.0.0 --port 8000` |
| Health checks | HTTP on `/healthz` (startup) and `/readiness` (steady state) |

Environment variables to include:

- `DATABASE_URL` → Render Postgres URL
- `REDIS_URL` → Render Redis URL
- `FRONTEND_ORIGIN` → your frontend hostname (e.g. `https://tms.hawkerboys.com`)
- `SECRET_KEY`, `SSG_*`, `DEFAULT_ADMIN_*`, and the remaining keys from `.env.example`

Enable auto-redeploy on image push or Git commits as desired.

## 4. Background Worker

Create a second Docker service from the same repository/image.

| Setting | Value |
| --- | --- |
| Start command | `rq worker ssg-sync` |
| Environment | Reuse the exact variable set from the web service |

This worker consumes the Redis queue used by SSG sync jobs.

## 5. Static Frontend

Use Render Static Sites pointed at `/frontend`.

| Setting | Value |
| --- | --- |
| Build command | `npm ci && npm run build` |
| Publish directory | `dist` |
| Environment variables | `VITE_API_URL=https://<backend-host>/api` (match your API URL) |

Upload the favicon and apple-touch icons packaged under `frontend/public`. Configure the custom domain and ensure HTTPS is enabled.

## 6. Environment variable checklist

Required keys (see `.env.example` for defaults):

- `APP_ENV`
- `API_HOST`, `API_PORT`
- `SECRET_KEY`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `REFRESH_TOKEN_EXPIRE_MINUTES`
- `PASSWORD_HASH_SCHEME`
- `FRONTEND_ORIGIN`
- `DATABASE_URL`
- `REDIS_URL`
- `RQ_DEFAULT_QUEUE`
- `SSG_BASE_URL`, `SSG_CLIENT_ID`, `SSG_CLIENT_SECRET`, `SSG_WEBHOOK_SECRET`, `SSG_ENV`
- `DEFAULT_ADMIN_EMAIL`, `DEFAULT_ADMIN_PASSWORD`
- `SENTRY_DSN` (optional)

## 7. Post-deploy checks

1. `curl https://<backend-host>/healthz` and `/readiness` should return HTTP 200.
2. Visit the frontend, sign in with the default admin credentials, and confirm the dashboard renders.
3. Create a course, verify it appears on the `/courses` page, and ensure a row is appended to `/v1/audit`.
4. Hit `POST /ssg/test-webhook` with the configured secret to confirm the security check.

## 8. Rollback

- Keep the previous backend Docker image tag. If needed, redeploy it via Render’s rollback UI.
- Restore the latest Postgres snapshot before rerunning migrations.
- If the worker misbehaves, scale it down to 0 replicas while the API stays online, then redeploy.
