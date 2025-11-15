# SSG Error Catalog

| SSG Error | Meaning | Operator Action | Technical Notes |
| --- | --- | --- | --- |
| `401 Unauthorized` | Credentials invalid or expired. | Check if client ID/secret changed. Re-run `make preflight`. | Rotate secrets, update hosting platform, confirm clock skew < 30s. |
| `403 Forbidden` | Account lacks permission for endpoint. | Confirm course is approved for submission and credentials have the required scopes. | Some endpoints require production whitelisting. Refer to SSG onboarding email. |
| `404 Not Found` | Referenced course/run/session absent. | Verify SSG course code and run ID. Ensure prior sync succeeded. | Review audit logs to ensure we stored the SSG identifiers; re-sync if missing. |
| `409 Conflict` | Duplicate submission detected. | Review if the item was already synced. If so, no action required. | Include idempotency keys when available; our client retries with same payload. |
| `422 Validation Failed` | Payload schema mismatch or invalid data. | Check field lengths, mandatory attributes, and NRIC masking. Correct locally and requeue job. | Enable debug logging temporarily to inspect sanitized payloads. Do not leak NRIC or secrets. |
| `429 Too Many Requests` | Rate limit exceeded. | Wait 15 minutes before retrying manually. Inform staff that sync will resume automatically. | Our client backs off exponentially up to 3 retries; consider staggering manual submissions. |
| `5xx Server Error` | SSG platform issue. | Continue operations offline. Notify SSG support if outage persists beyond 2 hours. | Jobs remain queued; monitor and reprocess once SSG recovers. |
| `INVALID_TOKEN` | OAuth token rejected. | Trigger new token by clearing worker cache (`rq flush`). | Inspect authentication request/response to ensure `grant_type` is `client_credentials`. |
| `MISSING_FIELD` | Required field blank. | Refer to the API docs for required fields. Update local record, resubmit. | Map the field to our schema and ensure migrations include it going forward. |
| `SSG-RATE-CONTROL` | Custom throttle warning. | Slow down manual submissions, schedule retries during off-peak hours. | Capture `Retry-After` header and configure worker delay accordingly. |

Use these steps when reviewing worker logs. Record corrective actions in the incident log if the same error repeats three times in 24 hours.
