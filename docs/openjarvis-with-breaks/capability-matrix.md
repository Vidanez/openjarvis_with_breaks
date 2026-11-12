# Capability admission matrix

This matrix is the admission contract for `openjarvis_with_breaks`. A listed capability is not enabled by this document; it records the evidence and controls required before a later slice may enable it. Unlisted capabilities are denied.

## Baseline

| Control | Contract |
| --- | --- |
| Default state | All side-effecting channels, cloud providers, MCP, uploads, shell, filesystem, and automatic learning are off. |
| Authority | Only an authenticated owner may request an admitted capability. Inbound content and model output are untrusted. |
| Effects | A send, write, delete, schedule, or change requires a sealed one-time owner approval and receipt, unless a complete bounded automation policy matches. |
| Cost | Default monthly cloud model/provider cap is **USD 0**. A nonzero cap requires immutable owner approval evidence and explicit configuration in a later implementation slice. |
| Budget failure | At cap, uncertain usage, missing metering, or provider-admission failure: reject new provider calls fail-closed; do not queue, substitute, or silently fall back to another provider. |
| Secrets | Tokens and session state belong in a governed runtime secret boundary, never source control, documentation, or ordinary logs. |

## Capability profiles

| Profile | Default | Allowed purpose and boundary | Admission evidence required | Effect rule |
| --- | --- | --- | --- | --- |
| Local model | Off | Owner tasks within the local runtime; no implied access to tools or external data | Model/version, runtime resource budget, data handling, tool boundary, operational owner approval | No effect without a separate admitted capability and transaction |
| Approved cloud provider | Off | Explicitly classified owner data only; provider is not a general fallback | Provider and model, region, retention/training policy, data class, token/rate cap, monthly cap, metering method, outage/fail-closed behavior, owner approval receipt | Provider invocation is denied when any admitted bound is absent or exceeded |
| MCP service | Off | One named service with declared, minimal permissions | Service identity, version/hash, endpoint, permission set, data classes, owner approval, audit fields, expiry/review, kill switch if effecting | Reject arbitrary URLs and stdio commands; downstream effects still require their own transaction |
| Sandboxed filesystem | Off | A named, minimal workspace needed by an admitted task | Allowed paths, read/write mode, mount isolation, owner approval, audit policy, expiry/review | Writes require a sealed owner approval unless a matching automation policy explicitly permits them |
| Sandboxed shell | Off | A fixed, isolated command boundary for an admitted task | Command allowlist, image/runtime, network policy, mounts, secret policy, resource limits, owner approval, audit policy | No arbitrary commands; any external mutation needs its own transaction |
| Google read-only | Off | Narrow Gmail, Calendar, or Drive reads explicitly selected by scope | OAuth scope list, corpus/sync boundary, token custody, data retention, owner approval, revocation handling | No Google mutation is implied by read access |
| Google write | Off | Exact Gmail send/delete, Calendar mutation, or Drive mutation capability | Explicit OAuth write scope, capability profile, token custody, target/data boundary, audit receipt schema, owner approval | Every mutation needs one matching sealed approval and one execution receipt |
| Baileys WhatsApp | Off | Isolated owner-scoped profile only; inbound content is untrusted | Dedicated profile, owner/chat allowlists, mode, session-state custody, retention/audit plan, account-risk acknowledgement, kill switch, owner approval | `manual_approval` requires a receipt per send; `automatic_reaction` requires a fully matching bounded policy |
| Meta WhatsApp Cloud API | Future draft | Preferred future production messaging path; not enabled in this project slice | Separate capability review, provider terms/data controls, channel identity, webhook trust model, receipt/audit and kill-switch design | No send or webhook action until separately admitted |
| Uploads and attachments | Disabled | No handling until a quarantine pipeline exists | Size/MIME detection, nested archive policy, malware scanning, no-network/no-secret parser sandbox, rendered-text policy, owner admission | Reject before parsing or storage outside the quarantine design |

## Provider budget and admission record

A later implementation must persist an admission record for each cloud provider/model. It must include the provider/model identifiers, region, permitted data classes, retention and training policy, pricing and meter source, monthly cap, token and concurrency limits, reset period, approval receipt reference, and disable state. The record is invalid if any required item is absent, expired, or inconsistent with the current request.

The default cap of USD 0 means no cloud request may leave the runtime. Increasing it is a new owner decision, not a configuration convenience. The implementation must reserve or account for usage before dispatch when possible and deny dispatch when it cannot establish that the cap will be respected.

## Automation-policy boundary

Automation is exceptional, not an alternative to approval. A policy must bind exactly one owner, capability, channel, contact allowlist, allowed intent, response boundary or template, start/end time, rate limit, expiry, budget, and emergency disable state. It must not grant task creation, memory changes, approval creation, tool authority, cross-channel effects, or broader recipient access.

For Baileys, group chats are rejected by default. `automatic_reaction` may only send a bounded response to a named allowlisted chat during the policy window. Baileys remains off unless its own profile is enabled; Meta Cloud API remains a separate future admission.

## Admission checklist

- [ ] The capability has a named profile and owner-approved purpose.
- [ ] Its input provenance and allowed data class are explicit.
- [ ] Least permissions, limits, retention, and secret custody are documented.
- [ ] Effects have immutable approvals/receipts or a matching bounded automation policy.
- [ ] Cost/provider limits meter before dispatch and fail closed.
- [ ] An expiry, review point, and immediate disable mechanism are defined.
