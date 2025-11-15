# SSG Error Catalog

| Raw Code / Message | Meaning | What to Check | Next Steps |
| --- | --- | --- | --- |
| 400 `invalid_payload` | Request malformed. | Ensure mandatory fields match SSG schema. | Fix data, retry job. |
| 401 `invalid_client` | OAuth credentials rejected. | Verify client ID/secret and environment. | Rotate credentials, run preflight. |
| 403 `insufficient_scope` | Token lacks permissions. | Check SSG portal access scopes. | Request required scope or use correct client. |
| 404 `resource_not_found` | Course/run missing in SSG. | Confirm codes align with SSG references. | Resubmit course creation first. |
| 409 `duplicate_entry` | Entity already registered. | Search SSG portal for existing record. | Update local record with SSG ID and retry update flow. |
| 422 `validation_failed` | Field failed SSG business rules. | Review response details in logs. | Correct local data, requeue job. |
| 429 `too_many_requests` | Rate limit hit. | Check job frequency and concurrency. | Wait 5 minutes, queue retries automatically. |
| 500+ `server_error` | SSG issue. | None. | Retry automatically, escalate if persistent. |

**Operator Tip**: Provide plain description to staff, but include correlation ID from logs when escalating to engineering.
