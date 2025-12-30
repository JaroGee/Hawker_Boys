# Role Permissions Matrix

Roles cover minimum TMS operations with least-privilege defaults. All actions are logged with correlation IDs; audit logs are immutable.

| Permission Area | Admin | Ops Admin | Trainer | Finance | Read-only Auditor |
| --- | --- | --- | --- | --- | --- |
| Manage users/roles | ✓ | ✓ (assign predefined roles) | ✗ | ✗ | ✗ |
| Configure courses and runs | ✓ | ✓ | ✗ | ✗ | View only |
| Manage sessions (schedule/venue/trainer) | ✓ | ✓ | Update assigned sessions | ✗ | View only |
| Enrol trainees | ✓ | ✓ | ✗ | ✗ | View only |
| Update/cancel enrolments | ✓ | ✓ | ✗ | Fee adjustments only with audit | View only |
| Record attendance | ✓ | ✓ | ✓ (assigned runs) | ✗ | View only |
| Submit/reconcile attendance | ✓ | ✓ | ✓ (assigned runs) | ✗ | View only |
| Capture assessments | ✓ | ✓ | ✓ (assigned runs) | ✗ | View only |
| Void/update assessments | ✓ | ✓ | Limited to own sessions | ✗ | View only |
| Manage fees/invoices | ✓ | ✓ (review) | ✗ | ✓ | View only |
| View compliance dashboard | ✓ | ✓ | ✓ (own runs) | ✓ | ✓ |
| View audit logs | ✓ | ✓ | ✗ | ✗ | ✓ (read-only) |

## Notes
- Trainers are restricted to course runs and sessions they are assigned to.
- Finance can adjust fee states but cannot alter enrolment eligibility fields.
- Read-only Auditor can view all entities and audit logs but cannot mutate data.
- Admin privileges should be tightly controlled; prefer Ops Admin for daily operations.
