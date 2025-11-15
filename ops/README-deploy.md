# Deployment Guide

## Prerequisites
- Docker and docker-compose v2.
- Access to hosting environment (Railway, Render, or AWS Lightsail).

## Local Compose
1. Copy `.env.example` to `.env` and set secrets.
2. Run `docker compose -f ops/docker-compose.yml up --build`.
3. Backend accessible at `http://localhost:8000`, frontend at `http://localhost:5173`.

## Railway
1. Provision PostgreSQL and Redis add-ons.
2. Deploy backend service using `ops/backend.Dockerfile`.
3. Add worker service with same image but command `rq worker ssg-sync`.
4. Deploy frontend using `ops/frontend.Dockerfile` as static service.
5. Configure environment variables in Railway settings.

## Render
1. Create Web Service from Git repo pointing to `/backend` with start command `uvicorn tms.api:app --host 0.0.0.0 --port 8000`.
2. Add Background Worker with command `rq worker ssg-sync` and same environment.
3. Add Managed PostgreSQL and Redis services; capture connection URLs.
4. Configure health checks to `/healthz` and `/readiness`.

## AWS Lightsail
1. Launch Docker container service or EC2 instance.
2. Install Docker (`sudo apt-get install docker.io`) and docker-compose plugin.
3. Use provided compose file; store secrets in AWS Secrets Manager or Parameter Store and inject via environment.
4. For PostgreSQL, use Lightsail managed database or Amazon RDS.

## Backups
- Automate `pg_dump -Fc` to S3 with lifecycle policies.
- Test restore with `pg_restore --clean --if-exists` quarterly.

## Monitoring
- Enable CloudWatch or equivalent log shipping.
- Configure uptime checks hitting `/healthz`.

## Disaster Recovery
1. Restore DB snapshot.
2. Redeploy containers from Git revision.
3. Re-run `make preflight` to confirm environment.
