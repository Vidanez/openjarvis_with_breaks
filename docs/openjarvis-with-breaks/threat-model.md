# Threat model: authority stays with the owner

The primary security objective is to prevent untrusted content from gaining authority and to prevent external effects without a precise owner-controlled authorization path. This document defines the threats Slice 0 requires later implementation slices to test and enforce.

## Assets and trust boundaries

| Asset | Security property |
| --- | --- |
| Owner authority | Only authenticated owner interactions can request tasks, memory changes, capability admission, approvals, or automation policies. |
| External-effect integrity | Sends, writes, deletes, schedules, and changes match an immutable transaction and produce one execution receipt. |
| Secrets and session state | OAuth tokens, messaging state, keys, and credentials remain in the runtime secret boundary. |
| Memory integrity | Memory is attributable, reviewable, expirable, and erasable; untrusted input cannot create it. |
| Capability boundary | Providers, Google scopes, MCP, shell, filesystem, uploads, and channels are explicit allowlist admissions. |
| Cost and privacy boundary | Provider data export and spending remain within a current approved admission record. |

Trust boundaries occur at the Open WebUI/API authentication edge; every connector/channel/attachment/webhook ingestion path; model and tool outputs; memory admission; capability dispatch; the approval/automation decision; and every remote deployment or secret-store boundary.

## Threat scenarios and required controls

| Scenario | Attacker path | Required control | Expected result |
| --- | --- | --- | --- |
| Email prompt injection | Mail body asks the agent to send, delete, disclose, or change policy | Classify connector content as untrusted; do not derive authority from text | Content may be shown as data but cannot create task, memory, approval, or effect |
| Document or link injection | Drive text, attachment, or webpage embeds instructions | Attachments remain disabled; other content is untrusted and cannot cross authority boundaries | No parser/content path grants tools, memory, or capability access |
| Webhook impersonation | Payload claims to be the owner or requests an urgent action | Authenticate the source separately; payload remains data | No owner identity or effect authority is inferred |
| Model-output tool injection | Model output asks to invoke a tool or relax policy | Treat model output as untrusted; validate tools against admission and effect gate | No tool or effect executes on output alone |
| Approval replay or mutation | Reuse a receipt, alter target/payload, use wrong owner, or execute after expiry | Bind approval to immutable payload, owner, nonce, idempotency key, and TTL; revalidate before execution | Request is denied; a receipt is single-use and exact-match only |
| Automation-policy overreach | Broaden recipient, intent, time window, rate, channel, or response content | Match all policy fields exactly; enforce expiry, budget, and kill switch | Out-of-scope request is denied without fallback |
| OAuth token exposure | Token is committed, logged, backed up insecurely, or used after revocation | Runtime secret interface, redaction, narrow scopes, reauthorization disables connector | No secret appears in source/docs/logs; affected connector fails closed |
| Provider data/cost escape | Send unapproved data, exceed cap, or substitute a provider | Admission record binds region/retention/data class/model/limits; default USD 0 cap; metering fail-closed | Dispatch is denied when admission or usage proof is absent |
| MCP or shell escape | Use arbitrary URL, stdio command, path, mount, or network | Named admission with version/hash, permissions, sandbox, and allowlists | Unadmitted service/command/path is denied |
| Attachment parser compromise | Malicious file exploits parser or exfiltrates secrets | Keep attachment handling disabled pending quarantine and no-network/no-secret sandbox | Attachment is rejected; no parser runs in this slice |
| WhatsApp social engineering | Inbound sender induces memory, tools, or automatic messaging | Keep Baileys off; classify inbound messages as untrusted; use allowlists and explicit modes only | No authority is created; default group-chat behavior is deny |
| Remote exposure | Public listener, unauthenticated UI, or broad firewall exposes service | Loopback bind; future named Cloudflare Tunnel plus Access; no public listener | Direct public inbound application access is denied |
| Backup rollback bypass | Restore revives expired authority or exposes secrets | Encrypted controlled backups; restore test preserves current policy and disables expired/revoked state | Restore does not reactivate approval, automation, or revoked access |

## Security invariants

1. Only an authenticated owner interaction can request a task, memory change, or external effect.
2. Email, documents, attachments, links, webhooks, WhatsApp inbound content, and model output are untrusted data, never instructions.
3. Every effect has either one matching owner approval and receipt or one complete matching automation policy.
4. Low-risk learning is limited to owner-originated preferences and remains reviewable, expirable, and erasable.
5. Google read/write access uses explicit profiles; every mutation has a sealed approval and receipt.
6. Attachments are disabled until a sandboxed quarantine pipeline exists.
7. Capability access is allowlist-based and governed by cost and privacy admission records.
8. Baileys is disabled by default; when separately admitted, it is isolated, owner-scoped, auditable, immediately disableable, and restricted to manual approval or policy-bounded automatic reaction. Meta Cloud API is a separate future production integration.

## Test matrix for later slices

Every implementation slice that crosses a boundary must include negative tests for at least the applicable rows below.

| Boundary | Minimum rejection cases |
| --- | --- |
| Untrusted content | Email, Drive/document text, link text, webhook payload, WhatsApp inbound text, and model output each attempt task, memory, approval, tool, and capability escalation |
| Approval | Replay, expiry, payload mutation, wrong owner, destination mismatch, and duplicate idempotency key |
| Automation | Contact mismatch, group-chat default rejection, intent mismatch, response-boundary mismatch, out-of-window execution, rate breach, budget breach, expiry, and kill switch |
| Provider | Missing admission field, incorrect data class/region/model, exhausted cap, unavailable metering, and fallback attempt |
| Google | Missing approval, mutated payload, replayed/expired receipt, wrong owner, revoked credential, and unadmitted scope |
| MCP/sandbox | Undeclared URL, stdio command, version/hash mismatch, path escape, forbidden mount/network, and missing admission |
| Restore | Expired approval/policy and revoked connector remain unusable after recovery |

## Out of scope in Slice 0

This is a policy contract, not a claim that controls already exist in the runtime. It does not implement a sandbox, quarantine pipeline, secret store, remote deployment, messaging integration, Google connection, provider configuration, or incident-response system. Those capabilities remain denied until later slices implement and test their corresponding controls.

## Review checklist

- [ ] Each new integration identifies its authority and data boundaries before it is enabled.
- [ ] New effects add abuse, replay, mutation, and mismatch tests.
- [ ] No untrusted input can create authority by prompt, metadata, or claimed identity.
- [ ] Failing infrastructure, metering, or authentication produces denial rather than a permissive fallback.
