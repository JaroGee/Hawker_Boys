# Security & Privacy Posture

## Identity & Access
- NextAuth with credential login for admins (bcrypt hashed) and magic links for other roles
- Middleware protects `/dashboard/*` and `/admin/*`
- RBAC helpers in `lib/auth/roles.ts`
- Audit events logged in `AuditEvent`

## Data protection
- Sensitive uploads stored through `lib/storage.ts`; optional AES-256-GCM if `FILE_ENCRYPTION_KEY` is set
- Documents scoped to owner plus admins, with mentor exceptions coded per module requirements
- PDPA minimisation: only necessary contact info stored

## Anti-abuse
- Cloudflare Turnstile on public feedback
- `lib/rate-limit.ts` handles in-memory throttling; set `RATE_LIMIT_REDIS_URL` to back with Redis in prod
- Public POST responses avoid leaking internals

## Transport & headers
- Next.js defaults to HTTPS on Vercel. Add `next-safe` middleware or security headers via `@next/headers` as needed
- Always deploy behind TLS (portal.hawkerboys.com)

## Logging & monitoring
- Magic link emails logged in dev only
- Audit log surfaces actions in admin dashboard
- Extend by shipping structured logs to Datadog or CloudWatch

## Incident response
1. Revoke compromised sessions via database update (`DELETE FROM Session`)
2. Rotate `NEXTAUTH_SECRET` and email provider credentials
3. Invalidate signed URLs by rotating `FILE_ENCRYPTION_KEY`
4. Notify stakeholders under PDPA timelines
