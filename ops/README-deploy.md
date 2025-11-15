# Deployment Guide

## 1. Prerequisites
- Docker 24+
- Access to container registry (e.g., GitHub Container Registry).
- Provisioned PostgreSQL 15+ and Redis 7 instances in Singapore region.
- SSG sandbox credentials stored securely.

## 2. Local Validation
1. Copy `.env.example` to `.env` and populate secrets.
2. Run `make preflight` to ensure DB, Redis, and SSG credentials are reachable.
3. Execute `make test` to confirm unit tests and linting pass.

## 3. Container Build and Push
```bash
# Backend
DOCKER_IMAGE=ghcr.io/hawker-boys/tms-backend:$(git rev-parse --short HEAD)
docker build -f ops/dockerfiles/backend.Dockerfile -t "$DOCKER_IMAGE" .
docker push "$DOCKER_IMAGE"

# Frontend
FRONTEND_IMAGE=ghcr.io/hawker-boys/tms-frontend:$(git rev-parse --short HEAD)
docker build -f ops/dockerfiles/frontend.Dockerfile -t "$FRONTEND_IMAGE" .
docker push "$FRONTEND_IMAGE"
```

## 4. Railway Deployment Steps
1. Create new PostgreSQL and Redis services.
2. Add a service for backend using Docker image above, configure environment variables, set health checks `/healthz`.
3. Add a worker service running `rq worker ssg_sync` with same image.
4. Deploy frontend using static site (upload `frontend/dist`).
5. Configure custom domain with HTTPS.

## 5. Render Deployment Steps
1. Create Render Postgres and Redis.
2. Deploy backend as Web Service with start command `uvicorn tms.main:app --host 0.0.0.0 --port 8000`.
3. Configure environment variables and secrets.
4. Add Background Worker with command `rq worker ssg_sync`.
5. Deploy frontend as Static Site with build command `npm install && npm run build`, publish `frontend/dist`.

## 6. AWS Lightsail Blueprint
1. Provision Lightsail container service in ap-southeast-1.
2. Build and push backend + worker images, deploy as separate containers.
3. Use Lightsail managed database for PostgreSQL, attach private networking.
4. Configure HTTPS via Lightsail Load Balancer and attach backend container.
5. Schedule nightly snapshots for disaster recovery.

## 7. Backup & Restore Procedures
- **Backup**: `pg_dump --no-owner --format=custom $DATABASE_URL > backup_$(date +%F).dump`
- **Restore**:
  ```bash
  pg_restore --clean --no-owner --dbname=$DATABASE_URL backup_xx.dump
  ```
- Store backups on encrypted S3 bucket or Railway storage with lifecycle policies.

## 8. Preflight Checklist (make preflight)
- Validates presence of mandatory environment variables.
- Confirms PostgreSQL connectivity and pending migrations.
- Checks Redis queue availability.
- Attempts OAuth token request to SSG sandbox (skipped if offline flag set).

## 9. Rollback Strategy
- Keep previous container images tagged and available.
- Maintain last known good database snapshot.
- If deployment fails, redeploy prior image and restore snapshot if schema changes occurred.

## 10. Post-Deployment Verification
- Hit `/healthz` and `/readiness` endpoints.
- Login via admin UI and verify course creation works end-to-end.
- Confirm background worker processes a test sync job without errors.
