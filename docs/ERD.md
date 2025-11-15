# Entity Relationship Overview

```
Course 1---n CourseModule
Course 1---n ClassRun 1---n Session
ClassRun n---n Learner (via Enrollment)
Enrollment 1---n Attendance
Enrollment 1---n Assessment 1---1 Certificate
Session n---n Trainer (via SessionTrainer)
```

## Entities
- **Course**: core training offering, holds modules and class runs.
- **CourseModule**: module metadata with duration.
- **ClassRun**: scheduled instance with capacity and sessions.
- **Session**: dated lesson tied to optional module.
- **Trainer**: instructor with SSG trainer ID reference.
- **Learner**: participant with hashed identifier surrogate for NRIC.
- **Enrollment**: join table capturing status and SSG enrollment ID.
- **Attendance**: per session record referencing enrollment.
- **Assessment**: learner performance and pass/fail.
- **Certificate**: issued per assessment.
- **AuditTrail**: logs CRUD actions with actor role.

## Sequence Flows
### Course Creation & Publish
1. Ops user creates course locally.
2. System records audit entry and enqueues `sync_course` job.
3. Worker obtains SSG token and calls `/courses` endpoint (per sample code).
4. On success, store returned identifiers for traceability.

### Class Run Registration
1. Ops configures schedule and sessions.
2. `sync_class_run` job enqueued.
3. Worker submits payload to `/courses/courseRuns`.

### Learner Enrollment & Attendance
1. Ops enrols learner into class run.
2. `sync_enrollment` job posts to `/courses/courseRuns/enrolments`.
3. Attendance marking triggers `sync_attendance` posting to `/courses/courseRuns/sessions/attendance`.

### Claims Submission
1. Finance finalises claim data.
2. Job posts to `/courses/courseRuns/claims` with supporting document pointer.
3. Responses logged with correlation IDs for reconciliation.
