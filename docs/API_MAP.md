# API Map to TPGateway

Direct API references require confirmation from the official API Discovery. The mappings below describe intended operations and placeholders for exact products/endpoints.

## Environment and Auth
- Expected environments: UAT (sandbox) and Production. **MISSING INFO**: base URLs and environment switching guidance.
- Auth: likely OAuth2 client credentials with API key-style headers. **MISSING INFO**: token endpoint, scopes, and required headers.
- Include correlation IDs in `X-Correlation-ID` (or equivalent) on every outbound call.

## Course Runs
| Operation | TPGateway API Group | Expected Endpoint | Notes |
| --- | --- | --- | --- |
| Create course run | Course Runs / Schedule Management | `POST /course-runs` (placeholder) | Confirm payload fields for schedule, venue, trainer. **MISSING INFO** |
| Update course run | Course Runs / Schedule Management | `PUT /course-runs/{id}` (placeholder) | Must be idempotent; include versioning if required. **MISSING INFO** |
| Cancel course run | Course Runs / Schedule Management | `POST /course-runs/{id}/cancel` (placeholder) | Check required cancellation reasons. **MISSING INFO** |
| Get course run status | Course Runs / Schedule Management | `GET /course-runs/{id}` (placeholder) | Use for sync status reconciliation. **MISSING INFO** |

## Enrolments
| Operation | TPGateway API Group | Expected Endpoint | Notes |
| --- | --- | --- | --- |
| Create enrolment | Enrolment Management | `POST /course-runs/{id}/enrolments` (placeholder) | Validate trainee identifiers; ensure consent flags included. **MISSING INFO** |
| Update enrolment | Enrolment Management | `PUT /enrolments/{id}` (placeholder) | Confirm allowable fields for updates. **MISSING INFO** |
| Cancel/withdraw enrolment | Enrolment Management | `POST /enrolments/{id}/cancel` (placeholder) | Check withdrawal reasons and fee implications. **MISSING INFO** |
| Search/view enrolment | Enrolment Management | `GET /enrolments` with filters (placeholder) | Confirm filter fields and pagination. **MISSING INFO** |

## Attendance
| Operation | TPGateway API Group | Expected Endpoint | Notes |
| --- | --- | --- | --- |
| Submit attendance | Attendance Management | `POST /course-runs/{id}/attendance` (placeholder) | Confirm attendance code set and session identifiers. **MISSING INFO** |
| Get attendance status | Attendance Management | `GET /attendance/{submission_id}` (placeholder) | Use for reconciliation after submission. **MISSING INFO** |

## Assessments
| Operation | TPGateway API Group | Expected Endpoint | Notes |
| --- | --- | --- | --- |
| Submit assessment results | Assessment Management | `POST /course-runs/{id}/assessments` (placeholder) | Confirm result schema and pass/fail indicators. **MISSING INFO** |
| Update or void assessment | Assessment Management | `PUT /assessments/{id}` or `POST /assessments/{id}/void` (placeholder) | Verify allowed transitions and fields. **MISSING INFO** |
| Get assessment status/history | Assessment Management | `GET /assessments/{id}` (placeholder) | Include submission audit info if provided. **MISSING INFO** |

## Sync and Job Handling
- Use idempotency keys for create/update calls to prevent duplicates.
- Log request/response metadata with correlation IDs; store sync job references locally.
- **MISSING INFO**: any rate limits, retry-after headers, and webhook callbacks provided by TPGateway.
