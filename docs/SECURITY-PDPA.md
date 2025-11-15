# Security and PDPA Controls

## Data Protection Principles
- Collect only data mandated by SSG or essential for training operations.
- Hash NRIC-equivalent identifiers before storage using SHA-256 with salt.
- Mask sensitive fields in UI and restrict exports to authorised roles.

## Encryption
- Enforce HTTPS for all external traffic (managed by hosting provider).
- Use platform encryption at rest (Railway, Render, Lightsail volumes) plus PostgreSQL encryption options where available.

## Access Control
- Role-based access control: Admin, Ops, Trainer, Learner.
- Administrative actions require `admin` role; attendance updates limited to trainer/ops.
- Audit trail stored in `audit_trails` table with timestamps and actor metadata.

## Logging & Monitoring
- Structured logging with correlation IDs for SSG calls.
- Recommend forwarding logs to hosted ELK or CloudWatch.
- Enable Sentry (or similar) for exception tracking.

## Data Retention
- Active learner records retained for 5 years post-course completion.
- Archived records encrypted and purged annually.
- Provide deletion workflow for subject requests within 30 days.

## Incident Response
1. Detect anomaly via monitoring alert.
2. Contain by revoking compromised credentials and isolating impacted systems.
3. Assess scope, document evidence, notify stakeholders within 72 hours as per PDPA.
4. Recover from backups and strengthen controls.

## Key Rotation
- Store secrets in platform key vault (Railway variables, AWS Secrets Manager).
- Rotate `SECRET_KEY`, `SSG_CLIENT_SECRET`, DB credentials at least twice a year.
- Update `.env` or platform configuration followed by service restart.

## Preflight Checklist
Run `make preflight` before deployments to ensure environment integrity.

## Backup & Restore
- Nightly `pg_dump -Fc` to secure storage (S3 with lifecycle policies).
- Quarterly restore test using `pg_restore` to staging environment.

## Red Team Quick Wins
- Input validation enforced via Pydantic schemas.
- Rate limiting recommended for auth endpoints (e.g., 5 attempts per minute via proxy).
- CSRF protection required if server-rendered forms introduced.
