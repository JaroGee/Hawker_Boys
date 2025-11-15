# Data Model and Integration Flows

## Entity Relationship Overview
```mermaid
erDiagram
    COURSE ||--o{ MODULE : contains
    COURSE ||--o{ CLASS_RUN : offers
    CLASS_RUN ||--o{ SESSION : schedules
    CLASS_RUN ||--o{ ENROLLMENT : includes
    SESSION ||--o{ ATTENDANCE : records
    ENROLLMENT ||--o{ ASSESSMENT : evaluates
    ENROLLMENT ||--|| CERTIFICATE : awards
    USER ||--o| LEARNER : profile
    USER ||--o| TRAINER : profile
    TRAINER ||--o{ SESSION : leads
    ENROLLMENT }o--|| LEARNER : belongs
    AUDIT_TRAIL }|--|| USER : actor
```

- **Course** holds reusable module templates and high-level SSG course code.
- **ClassRun** references a course and captures run-specific metadata (start/end, status, SSG run ID).
- **Session** tracks session-level attendance and trainer assignments.
- **Learner** stores masked identifiers and contact details linked to optional user accounts for portal access.
- **Enrollment** links learners to class runs with status and SSG sync keys.
- **Attendance**, **Assessment**, and **Certificate** hang off enrollments for compliance artefacts.
- **AuditTrail** records sensitive CRUD and access events for PDPA traceability.

## SSG Sync Flows

### A. Course Creation and Publish
```mermaid
sequenceDiagram
    participant Ops
    participant API as TMS API
    participant Queue as RQ Queue
    participant Worker
    participant SSG as SSG API

    Ops->>API: POST /api/v1/courses
    API->>Queue: enqueue sync_course_to_ssg(course_id)
    Queue-->>Worker: job payload
    Worker->>SSG: POST /courses
    SSG-->>Worker: 201 Created / error
    Worker->>API: log outcome, update audit trail
```

### B. Class Run Registration
```mermaid
sequenceDiagram
    Ops->>API: POST /api/v1/courses/{id}/runs
    API->>Queue: enqueue sync_class_run_to_ssg(class_run_id)
    Worker->>SSG: POST /courses/courseRuns
    SSG-->>Worker: run identifier or error
    Worker->>DB: persist SSG run ID if provided
```

### C. Learner Enrollment and Attendance Submission
```mermaid
sequenceDiagram
    Ops->>API: POST /api/v1/enrollments
    API->>Queue: enqueue sync_class_run_to_ssg(class_run_id)
    Trainer->>API: POST /api/v1/attendance
    API->>Queue: enqueue sync_attendance_to_ssg(attendance_id)
    Worker->>SSG: POST /courses/runs/sessions/attendance
    SSG-->>Worker: response with correlation ID
    Worker->>Logs: store correlation + status
```

### D. Claims Submission (placeholder)
> Future enhancement: After SSG releases claims endpoint for providers, extend worker to submit attendance-derived claims and store claim references for reconciliation.
