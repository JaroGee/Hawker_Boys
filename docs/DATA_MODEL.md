# Data Model (ERD-level)

This document lists the core tables and relationships for the TMS MVP. Field names are indicative; confirm against TPGateway schemas where applicable.

## Entities and Key Fields
- **users**: id (PK), email, password_hash, status, created_at, updated_at.
- **roles**: id (PK), name (Admin, Ops Admin, Trainer, Finance, Auditor), description.
- **user_roles**: user_id (FK users), role_id (FK roles), unique constraint on pair.
- **trainees**: id (PK), name, contact info, national_id (masked storage), date_of_birth, consent_flags, created_at.
- **trainers**: id (PK), name, contact info, credentials, active_status.
- **course_runs**: id (PK), external_id (TPGateway reference), course_ref, title, start_date, end_date, delivery_mode, venue, capacity, status (draft/pending/synced/failed/cancelled), sync_version, created_at, updated_at.
- **sessions**: id (PK), course_run_id (FK course_runs), session_date, start_time, end_time, venue, trainer_id (FK trainers), status.
- **enrolments**: id (PK), course_run_id (FK), trainee_id (FK trainees), status (draft/pending/accepted/failed/cancelled), fee_amount, subsidy_info, sync_reference, sync_attempts, created_at, updated_at.
- **attendance_records**: id (PK), session_id (FK sessions), enrolment_id (FK enrolments), status (present/absent/late/unknown), reason, recorded_by, signed_off_at, sync_reference, sync_status.
- **assessments**: id (PK), enrolment_id (FK enrolments), assessment_type, score, result (pass/fail/void), assessed_at, assessor_id (FK trainers or users), sync_reference, sync_status, void_reason.
- **audit_logs**: id (PK), entity_type, entity_id, action, actor_id (FK users), correlation_id, payload_snapshot (JSON), created_at; immutable append-only.
- **sync_jobs**: id (PK), job_type, entity_type, entity_id, correlation_id, idempotency_key, status (queued/running/succeeded/failed/dead_letter), attempts, last_error, next_retry_at, created_at, updated_at.

## Relationships
- users ↔ roles: many-to-many via user_roles.
- course_runs ↔ sessions: one-to-many.
- course_runs ↔ enrolments: one-to-many.
- sessions ↔ attendance_records: one-to-many; attendance_records also link to enrolments for trainee context.
- enrolments ↔ assessments: one-to-many (versioned updates by status history).
- sync_jobs reference any entity by type/id for submission tracking.
- audit_logs link to entities and capture correlation IDs from requests/jobs.

## Indexing and Constraints
- Unique index on user email; ensure case-insensitive search.
- Unique constraint on (trainee_id, course_run_id) within enrolments to prevent duplicates.
- Foreign key constraints on session-to-course_run and attendance-to-session/enrolment.
- Index on sync_jobs.status and next_retry_at for efficient worker polling.
- Index on audit_logs.entity_type/entity_id for fast retrieval during investigations.
- Consider partial indexes for active course runs and active enrolments to speed dashboard queries.

## Data Protection
- Mask or tokenize national identifiers at rest; store only hashed/partial values if permissible.
- Avoid storing secrets; configuration values via environment variables/secret manager.
- Keep immutable audit_logs; do not allow updates or deletes.

## MISSING INFO
- Exact field names and types required by TPGateway for course runs, enrolments, attendance, and assessments.
- Any mandated identifiers (e.g., course reference formats, session IDs) and validation rules.
- Requirements for storing submission receipts or acknowledgement numbers from TPGateway.
