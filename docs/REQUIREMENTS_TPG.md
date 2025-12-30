# TPGateway Minimum Integration Requirements

This document captures the minimum integration scope for Hawker Boys TMS to align with SSG/WSG TPGateway guidance. Where details are unavailable offline, items are tagged under **MISSING INFO** for confirmation against the official FAQ and API Discovery.

## Assumptions
- Integration is limited to required compliance areas: Course Runs, Enrolments, Attendance, Assessments.
- TPGateway remains the system of record for regulated data submitted to the government; the TMS keeps an operational copy and sync metadata.
- All outbound calls must include correlation IDs for traceability and support immutable audit logging inside the TMS.

## Course Runs
- **Required operations**: create course run, update schedule/venue/trainer, cancel course run, query run status/sync errors.
- **Data fields and validation rules**:
  - Run identifiers, course reference, start/end dates, delivery mode, venue, trainer assignment, planned capacity (trainees). **MISSING INFO**: exact field names, date/time formats, accepted enumerations for delivery mode and venue type.
  - Validation should block submission of past-dated start times or capacities below existing enrolments; ensure timezones align with Singapore time.
- **Edge cases and failure handling**:
  - Handle duplicate submissions idempotently using client-generated keys to avoid double-creating runs.
  - On cancellation, ensure dependent enrolments and sessions are marked accordingly; retry transient API failures with exponential backoff.
  - Capture and surface partial validation errors returned by TPGateway.
- **Source of truth**:
  - TPGateway: canonical course run status and identifiers once accepted.
  - Local: draft runs, scheduling metadata before submission, and sync job history.
- **Operational notes**: FAQ references submission deadlines for course run updates prior to class start. **MISSING INFO**: exact cutoff windows and grace periods.

## Enrolments
- **Required operations**: create enrolment, update trainee particulars, cancel or withdraw, search/view enrolment status, report fee collection state.
- **Data fields and validation rules**:
  - Trainee identifiers, contact info, NRIC/FIN handling rules, course run linkage, subsidy eligibility, fee breakdown. **MISSING INFO**: mandatory vs optional fields, masking rules for national IDs, allowed fee components.
  - Enforce uniqueness per trainee per course run; ensure consent flags are captured before submission.
- **Edge cases and failure handling**:
  - Prevent over-enrolment beyond run capacity; reconcile when cancellations free capacity.
  - Handle pending subsidy verification states; retry submissions on transient errors; queue retries for network outages.
  - Record immutable audit log entries for any enrolment changes.
- **Source of truth**:
  - TPGateway: official enrolment acceptance and subsidy-related status.
  - Local: pre-submission drafts, payment tracking, and operational notes.
- **Operational notes**: FAQ highlights deadlines for enrolment submission relative to course start. **MISSING INFO**: specific lead times and cutoffs.

## Attendance
- **Required operations**: record attendance per session, reconcile totals, submit attendance to TPGateway, retrieve submission status.
- **Data fields and validation rules**:
  - Session date/time, trainee presence status, trainer sign-off, reasons for absence, make-up sessions. **MISSING INFO**: exact presence codes, tolerances for late attendance, digital signature requirements.
  - Validation: ensure sessions exist and enrolments are active; enforce no duplicate attendance for same trainee-session.
- **Edge cases and failure handling**:
  - Offline capture with delayed sync; handle session reschedules; support correction submissions with audit trail.
  - Reconcile discrepancies between local records and TPGateway by flagging runs for operator review.
- **Source of truth**:
  - TPGateway: accepted attendance submissions for compliance.
  - Local: real-time capture, pending submissions, reconciliation status.
- **Operational notes**: FAQ references attendance submission deadlines after session end. **MISSING INFO**: exact timeframes and penalties.

## Assessments
- **Required operations**: capture assessment results, submit to TPGateway, update/void results, view submission status/history.
- **Data fields and validation rules**:
  - Assessment type, score/pass-fail, assessment date, assessor identity, remarks. **MISSING INFO**: required grading scales, pass thresholds, attachment handling.
  - Ensure assessment date falls within course run; enforce one active result per trainee per assessment attempt, with versioned updates.
- **Edge cases and failure handling**:
  - Handle voiding/overwriting previous submissions with immutable audit logging.
  - Retry transient submission failures; queue dead-letter for repeated errors with operator escalation.
- **Source of truth**:
  - TPGateway: official assessment outcomes once accepted.
  - Local: operational drafts, assessor notes, and audit logs.
- **Operational notes**: FAQ notes timelines for submitting assessment results. **MISSING INFO**: precise deadlines and any appeal workflows.

## Compliance and Audit
- Maintain immutable audit logs for all key mutations: enrolment creation/changes, attendance edits, assessment updates, course run changes.
- Use structured logging with correlation IDs across API calls and background jobs for traceability.
- Support retries with backoff and dead-letter queues for failed submissions; expose reconciliation dashboards.

## MISSING INFO Summary
- Exact API endpoints, HTTP methods, and payload schemas for all operations (Course Runs, Enrolments, Attendance, Assessments).
- Specific submission deadlines and lead times mandated by TPGateway FAQ.
- Required headers/auth schemes (e.g., OAuth2 client credentials) and environment base URLs for UAT vs production.
- Enumerations and validation rules: delivery modes, venue types, NRIC/FIN formatting, attendance codes, assessment grading scales, subsidy fields, fee components, and digital signature requirements.
