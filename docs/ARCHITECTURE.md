# Architecture Overview

This document outlines the MVP architecture for Hawker Boys TMS aligned to TPGateway compliance requirements.

## Modules
- **Auth & RBAC**: JWT-backed auth with roles enforced at API and UI. Supports correlation IDs per request.
- **Course Runs**: Manage local course runs, session schedules, sync state with TPGateway.
- **Enrolments**: Capture trainee data, fee state, sync submissions, and status checks.
- **Attendance**: Session-level capture with reconciliation against TPGateway submissions.
- **Assessments**: Record assessment results, updates/voids, and submission tracking.
- **Compliance Dashboard**: Status rollups, deadline alarms, dead-letter visibility.
- **Audit Logs**: Immutable append-only records for key mutations (course runs, enrolments, attendance, assessments, fees, role changes).
- **Sync Jobs**: Background worker (RQ) handling retries, idempotency, and error capture.

## High-Level Architecture
```mermaid
graph TD
  UI[Frontend Ops UI] --> API[FastAPI Service]
  API --> Auth[Auth/RBAC]
  API --> SRV[Domain Services]
  SRV --> DB[(Postgres)]
  SRV --> Audit[Audit Log Store]
  SRV --> Queue[RQ Worker]
  Queue --> TPG[TPGateway APIs]
  SRV --> TPG
  SRV --> Metrics[Structured Logs + Metrics]
  Metrics --> Cloud[Observability]
```

## Sequence: Create Course Run
```mermaid
sequenceDiagram
  participant User
  participant UI
  participant API
  participant Service as CourseRunService
  participant Job as SyncJob/RQ
  participant TPG as TPGateway
  User->>UI: Submit new course run
  UI->>API: POST /course-runs (with correlation ID)
  API->>Service: validate + store draft
  Service->>Job: enqueue sync with idempotency key
  Job->>TPG: call create course run API
  TPG-->>Job: response (success/error)
  Job-->>Service: update sync status
  Service-->>UI: status updated + audit log recorded
```

## Sequence: Enrol Trainee
```mermaid
sequenceDiagram
  participant User
  participant UI
  participant API
  participant Enrol as EnrolmentService
  participant Job as SyncJob/RQ
  participant TPG as TPGateway
  User->>UI: Enrol trainee
  UI->>API: POST /enrolments (correlation ID)
  API->>Enrol: validate enrolment + ensure capacity
  Enrol->>Job: enqueue enrolment submission with idempotency key
  Job->>TPG: call enrolment API
  TPG-->>Job: submission result
  Job-->>Enrol: update status, fees, audit log
  Enrol-->>UI: status + sync result
```

## Sequence: Attendance Reconcile
```mermaid
sequenceDiagram
  participant Trainer
  participant UI
  participant API
  participant Att as AttendanceService
  participant Job as SyncJob/RQ
  participant TPG as TPGateway
  Trainer->>UI: Mark attendance for session
  UI->>API: POST /attendance
  API->>Att: validate session + enrolment state
  Att->>Job: enqueue submission
  Job->>TPG: submit attendance
  TPG-->>Job: response with submission id/status
  Job-->>Att: store status, reconcile discrepancies
  Att-->>UI: show pending/failed with retry option
```

## Sequence: Submit Assessment
```mermaid
sequenceDiagram
  participant Assessor
  participant UI
  participant API
  participant Assess as AssessmentService
  participant Job as SyncJob/RQ
  participant TPG as TPGateway
  Assessor->>UI: Enter assessment result
  UI->>API: POST /assessments (correlation ID)
  API->>Assess: validate attempt + scoring rules
  Assess->>Job: enqueue submission
  Job->>TPG: submit assessment result
  TPG-->>Job: response with status
  Job-->>Assess: store submission status + audit
  Assess-->>UI: display success/failure with retry
```

## Integration Patterns
- **Idempotency**: client-generated keys per submission; stored with sync jobs to prevent duplicates.
- **Retries/Backoff**: exponential backoff for transient errors; max attempts before dead-lettering.
- **Dead-Letter**: failed jobs captured with error context; surfaced on compliance dashboard for operator action.
- **Correlation IDs**: generated at UI, propagated through API, jobs, and outbound requests; logged in structured logs.
- **Structured Logging**: JSON logs including request ids, user, action, entity, result, latency.
- **Audit Trails**: append-only records with timestamps, actor, change summary, correlation ID, immutable by design.
- **Security**: never store secrets in code; use environment variables and secret manager; enforce RBAC on every endpoint.
