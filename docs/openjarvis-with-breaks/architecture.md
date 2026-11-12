# Secure owner-mediated assistant architecture

`openjarvis_with_breaks` uses OpenJarvis as its runtime core and Open WebUI as its initial user interface. The profile is a policy kernel around that runtime: it defaults to deny, separates authority from content, and requires a sealed approval or a narrowly bounded automation policy before an external effect can occur.

## Quick path

1. Accept tasks only from an authenticated owner interaction.
2. Classify every other input, including model output, as untrusted data.
3. Admit each capability explicitly; keep it disabled otherwise.
4. Seal every external effect to an immutable payload and obtain a one-time owner approval or a matching bounded automation policy.

## System boundary

```text
Authenticated owner ──> Open WebUI / loopback API ──> policy kernel ──> OpenJarvis runtime
                                                        │                 │
Untrusted sources ─────────────────────────────────────┤                 ├─ admitted capabilities
(email, documents, links, webhooks, WhatsApp, models)   │                 │  (models, Google, MCP, sandbox)
                                                        └─ audit receipts ─┘
```

OpenJarvis provides the internal agent, tool, connector, memory, and approval primitives. The `openjarvis_with_breaks` profile constrains their use. Open WebUI is the initial interface and does not itself grant authority. Future remote access must retain loopback application listeners and use Cloudflare Access with a named outbound Tunnel; it is not part of this slice.

## Authority and trust model

| Item | Classification | May request work | May change memory | May cause an effect |
| --- | --- | ---: | ---: | ---: |
| Authenticated owner command | authority-bearing | Yes | Subject to memory policy | Subject to approval or automation policy |
| Owner preference candidate | derived from owner command | No | Low-risk, reviewable only | No |
| Connector/channel content | untrusted data | No | No | No |
| Attachment, document, link, or webhook payload | untrusted data | No | No | No |
| Model output or tool result | untrusted data | No | No | No |
| Approval receipt | execution evidence | No | No | Only for its exact sealed action |

Untrusted content can be summarized, searched, and presented to the owner only through admitted read paths. It cannot create tasks, approvals, memory, capability changes, tool calls, automation policies, or cross-channel effects. Parsing content is not authorization.

### Owner identity

The profile has one configured, authenticated owner identity. Authentication is evaluated at the interface and action-approval boundaries; a display name, sender address, chat name, or text inside a message is never sufficient proof. A request from a non-owner source remains data even when it asks to impersonate the owner or claims urgency.

### Effect transaction

An effect includes a send, write, delete, schedule, configuration change, or equivalent external mutation. Before execution, the policy kernel must bind all of the following into an immutable transaction:

- authenticated owner identity;
- capability and target channel;
- exact destination, parameters, and rendered payload;
- single-use nonce, idempotency key, and expiry;
- applicable cost and rate bounds.

Execution is permitted only with one of these paths:

1. A matching, unexpired, one-time owner approval. The runtime revalidates the sealed transaction immediately before execution and stores an execution receipt.
2. A currently active automation policy whose complete scope matches the effect: owner, capability, channel, contact allowlist, intent, response boundary or template, time window, rate limit, expiry, budget, and kill-switch state.

Remembered approvals, silent "trivial" effects, payload substitution, and receipt reuse are invalid for this profile.

## Memory and retention

| Data class | Default handling | Review and deletion |
| --- | --- | --- |
| Owner-originated low-risk preference | May be proposed for automatic learning | Attributable, scoped, expirable, reviewable, correctable, and erasable by the owner |
| Task or action record | Retain only the minimum receipt/audit fields needed for traceability | Owner can review; follow the configured retention policy |
| Connector, document, attachment, link, webhook, and model content | No automatic memory admission | May be displayed or processed only by an admitted read path; never becomes memory by itself |
| OAuth tokens, session state, and secrets | Runtime secret boundary only | Not committed, logged, or placed in documentation; revoke/reauthorize through the owner-controlled flow |

Memory records must carry provenance, confidence, scope, review state, expiry, and deletion reason where applicable. Attachment ingestion remains disabled until the quarantine contract and implementation exist.

## Capability admission boundary

A capability is unavailable unless an explicit admission profile enables it. Admission is separate for provider/model execution, Google scopes, MCP services, sandboxed filesystem or shell access, and messaging channels. Admission must define the intended purpose, allowed data class, permissions, cost/privacy controls, owner approval rule, audit fields, expiry or review cadence, and kill switch where the capability can create effects.

The default profile admits no channel, upload, MCP server, cloud model, shell, filesystem path, or automatic learning path. Local model use is also explicit rather than implied by installation.

## Non-goals for Slice 0

- No runtime, connector, container, deployment, or profile configuration is implemented here.
- No OCI, Cloudflare, GitHub, Google, Meta, or WhatsApp resource is created or changed.
- No attachment ingestion, general shell/filesystem access, broad MCP discovery, or unattended messaging is enabled.
- No public application listener is introduced.

## Review checklist

- [ ] An authenticated owner is the only source of authority.
- [ ] Every external input and model output is treated as data, not instruction.
- [ ] Every effect has an exact approval receipt or a fully matching active automation policy.
- [ ] Memory remains attributable, reviewable, expirable, and erasable.
- [ ] Every capability is separately admitted and deny-by-default.
