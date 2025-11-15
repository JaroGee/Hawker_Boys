# Security and PDPA Playbook

## 1. Data Classification
- **Restricted**: Learner personal data, attendance, assessments.
- **Confidential**: Trainer profiles, course content, audit logs.
- **Internal**: System metrics, job queue stats.

## 2. Access Control
- JWT tokens issued via `/api/v1/auth/token` with 30-minute access lifespan and refresh via re-authentication.
- Roles:
  - **Admin**: full access, manage users and security settings.
  - **Ops**: manage courses, runs, enrollments, certificates.
  - **Trainer**: manage attendance and assessments for assigned sessions.
  - **Learner**: read-only profile access (future portal).
- Enforce principle of least privilege by assigning the lowest viable role.

## 3. Data Protection
- **Transport**: All public endpoints must sit behind HTTPS (enforce via hosting platform or ingress).
- **At Rest**: Use platform encryption (Render, Railway, Lightsail support). Enable disk encryption if self-managing infrastructure.
- **Field Level**: Store only masked NRIC (e.g., `S1234567*`). If full NRIC capture is mandated temporarily, encrypt with AES-256 and rotate keys quarterly.

## 4. Audit and Monitoring
- Every create/update/delete/access of sensitive entities records an `AuditTrail` entry with actor, entity, timestamp.
- Logs include request IDs and SSG correlation IDs (extend Loguru configuration if needed).
- Integrate Sentry or equivalent via `SENTRY_DSN` for error aggregation.

## 5. Data Retention
- Learner profiles: retain for 5 years after last class to satisfy SSG audit requirements.
- Attendance and assessments: retain for 6 years aligned with PDPA accountability.
- Audit trails: retain for 7 years for incident reconstruction.
- Provide anonymisation or deletion capability upon learner request once statutory period lapses.

## 6. Incident Response
1. Contain: Disable affected user accounts, revoke tokens, isolate compromised services.
2. Assess: Review audit logs, identify scope of data exposure.
3. Notify: Inform management and, if PDPA breach thresholds met, notify PDPC and impacted learners within 72 hours.
4. Eradicate: Patch vulnerabilities, rotate secrets, increase monitoring.
5. Recover: Restore services from clean backups, monitor for recurrence.
6. Lessons Learned: Document post-mortem and update training.

## 7. Backup and Restore
- Nightly `pg_dump` stored on encrypted storage.
- Test restore monthly using `pg_restore` into staging instance.
- Back up `.env` and secrets using secret manager exports (never commit to git).

## 8. Key Management
- Store secrets in platform secret stores (Render secrets, Railway variables, AWS Parameter Store).
- Rotate JWT secret, SSG credentials, and database passwords at least every 6 months or upon staff turnover.
- Document rotation steps in ops runbook and require two-person approval for production rotations.

## 9. Red-Teaming Quick Wins
- Rate limit authentication (e.g., 5 attempts per minute per IP) - integrate with FastAPI middleware or gateway.
- Validate all incoming data using Pydantic schemas; reject invalid NRIC formats.
- Enable CSRF protection if server-rendered forms are introduced.
- Conduct quarterly dependency audit using `pip-audit` and `npm audit --production`.

## 10. PDPA Rights Handling
- **Access Requests**: Export learner data from database within 30 days, redact other learners' details.
- **Correction Requests**: Update records via admin UI/API and log adjustments in audit trail.
- **Withdrawal of Consent**: Explain statutory retention obligations, document response.
