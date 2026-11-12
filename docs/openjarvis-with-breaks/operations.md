# Operational prerequisites and safe operation

Slice 0 defines gates for operating `openjarvis_with_breaks`; it does not deploy or configure a runtime. The service remains local and deny-by-default until all relevant gates are satisfied.

## Operating posture

| Area | Required posture |
| --- | --- |
| Runtime | OpenJarvis is the core; Open WebUI is the initial UI. Application listeners remain loopback-only. |
| Local validation | Use OrbStack for disposable local topology and profile validation before considering a cloud host. |
| Remote publication | Deferred. A later approved deployment must use a named outbound Cloudflare Tunnel and Cloudflare Access, not a public application listener. |
| External actions | Deny unless a sealed owner approval or full matching automation policy authorizes the exact effect. |
| Cloud models | Deny by default under the USD 0 monthly cap. |
| Attachments, MCP, shell, filesystem, and messaging | Disabled until individually admitted. |

## Provisioning gates

No OCI resource may be provisioned until every gate below is true and a new owner approval is recorded.

| Gate | Required evidence | Current classification |
| --- | --- | --- |
| OCI API authentication | Read-only authentication succeeds without exposing identifiers, key material, or debug output | Required before provisioning |
| Always Free capacity | A point-in-time report shows the approved exact shape in the home region/availability domain | Blocked: Madrid capacity has not admitted the required free shape |
| Cost and region review | Owner approves any shape, region, or pricing change; no Trial/PAYG credit is consumed by assumption | Required for any alternative |
| Runtime fit | Isolated benchmark demonstrates sufficient headroom for OS, Tunnel, Open WebUI, OpenJarvis, logs, backups, and approved model path | Not yet proven |
| Cloudflare publication | Named Tunnel and Access policy are reviewed; application stays loopback-only | Deferred |
| Backup and restore | Encrypted backup procedure and a successful restore test exist | Required before remote operation |
| Health and rollback | Health checks, restart behavior, alerting boundary, and rollback procedure are tested | Required before remote operation |

Capacity reports do not reserve hosts. If the approved capacity is unavailable, retain the deployment design and stop; do not substitute a paid resource, a different region, or a different allocation without a new owner decision.

## Local validation runbook

1. Start only a disposable local environment through OrbStack after the later profile implementation exists.
2. Confirm application services bind only to loopback.
3. Confirm the secure profile starts with channels, uploads, MCP, cloud providers, shell, filesystem, and automatic learning disabled.
4. Exercise owner authentication, untrusted-content classification, denied effects, budget exhaustion, receipt replay rejection, and emergency-disable behavior using non-production test data.
5. Record only sanitized pass/fail evidence. Do not collect credentials, tokens, identifiers, payloads, or raw debug logs in repository documentation.
6. Destroy disposable test state when validation completes.

## Health, backup, and restore contract

A later deployment must provide a minimal health signal for the process, policy-kernel availability, storage availability, and backup freshness without revealing sensitive content. Health failure must not weaken the deny-by-default policy or trigger an automatic capability fallback.

Backups must be encrypted, access-controlled, and bounded to the minimum runtime state required for recovery. A restore test must prove that the recovered instance maintains loopback binding, secret separation, disabled-by-default capabilities, and audit/approval integrity. Backup restore does not revive expired approvals, receipts, automation policies, revoked credentials, or disabled capabilities.

## Incident and rollback rules

| Event | Immediate action | Recovery condition |
| --- | --- | --- |
| Suspected credential or session-state exposure | Disable affected connector/profile, revoke or reauthorize through the owner-controlled path, preserve only sanitized incident evidence | Secret boundary is re-established and owner explicitly readmits the capability |
| Untrusted-content authority attempt | Reject the request, retain minimal sanitized audit metadata, review boundary coverage | Test or control demonstrates the content remains data-only |
| Budget/metering uncertainty | Stop provider dispatch and disable the provider profile | Metering and cap enforcement are verified against the approved admission record |
| Approval or automation mismatch | Reject execution; do not retry with relaxed scope | New exact approval or matching active policy exists |
| Messaging concern | Use the kill switch; disable Baileys/profile immediately | Dedicated review confirms allowlists, policy bounds, and audit controls |
| Failed deployment or health check | Roll back to the last known safe local-only state; keep external capabilities disabled | Health, loopback, backup, and rollback checks pass |

## Operational checklist

- [ ] No cloud or remote deployment proceeds while OCI capacity, cost, or runtime-fit gates are unresolved.
- [ ] Cloudflare Access/Tunnel is reviewed before any remote publication.
- [ ] Backups are encrypted and a restore test has passed.
- [ ] Health checks cannot disclose secrets or enable fallbacks.
- [ ] Provider budgets, capability disable controls, and effect receipts fail closed.
- [ ] Operational records exclude credentials, keys, personal identifiers, and raw logs.
