# Hawker Boys Portal

A Next.js 14 App Router experience for trainees, mentors, employers, and admins. Matches the www.hawkerboys.com brand system while staying PDPA-conscious.

## Prerequisites
- Node.js 20 (use `nvm use` or `fnm use` as per company standards)
- npm 10 (`corepack enable` recommended)
- SQLite available locally (bundled with Prisma)

## Quick start
1. `cp .env.example .env`
2. `npm install`
3. `npm run prisma:generate`
4. `npm run db:migrate`
5. `npm run db:seed`
6. `npm run dev`

Visit http://localhost:3000. Sign in with `admin@hawkerboys.com` / `ChangeMe123!` (change immediately) or request a magic link for seeded users.

## Scripts
- `npm run dev` – Next dev server with hot reload
- `npm run build` – Production build output `.next/`
- `npm run start` – Serve the production bundle
- `npm run lint` – ESLint via `next lint`
- `npm run test` – Vitest unit tests (placeholder)
- `npm run prisma:generate` – Generate Prisma client
- `npm run db:migrate` – `prisma migrate dev --name init`
- `npm run db:seed` – Seed demo data via `tsx prisma/seed.ts`

## Data model snapshot
Prisma models cover:
- `User` with role enum and optional password hash
- Profile tables for `Trainee`, `Mentor`, `Employer`
- Announcements, quests, badges, assessments, support tickets
- Secure documents and emergency contacts
- Live location sessions and audit events

Inspect `prisma/schema.prisma` for full definitions.

## Dev database
Default `DATABASE_URL` uses SQLite (`file:./prisma/dev.db`). Delete the file to reset. For Postgres, update both the env var and `prisma/schema.prisma` provider then re-run migrations.

## Storage
During dev files land in `.uploads/`. Set S3 env vars for R2 or AWS when deploying. Add `FILE_ENCRYPTION_KEY` (hex) to encrypt sensitive buffers.

## Magic link email
If `RESEND_API_KEY` or `POSTMARK_API_TOKEN` is missing, verification URLs are logged via `console.info('[magic-link]', ...)`. On staging, set either provider and a verified `from` address.

## Screenshots
See `/docs/screenshots` (to be captured after UI polish) for stakeholder-ready visuals.

## Troubleshooting
- Prisma errors: delete `node_modules`, run `npm install`, then `npm run prisma:generate`
- NextAuth secret missing: re-run `openssl rand -base64 32` and set `NEXTAUTH_SECRET`
- Styles missing: confirm `tailwind.config.ts` `content` globs include new folders
- Seed idempotency: re-run `npm run db:seed` anytime; tables are truncated in script
