# openjarvis_with_breaks Implementation Plan

> **For Hermes:** Execute this plan through fresh delegated work units with an independent verification after each slice.

**Goal:** Turn the `Vidanez/openjarvis_with_breaks` fork into an owner-mediated personal assistant that preserves normal OpenJarvis model, engine, tool, MCP, and memory behavior while adding a concise trust boundary for external effects.

**Architecture:** OpenJarvis remains the runtime and its supported engine and provider choices remain available. The fork adds provenance-aware handling around external actions: authenticated owner conversations can learn preferences and produce suggestions; external content and model output can produce attributed proposals for the owner but cannot autonomously cause an external side effect or grant permissions. Open WebUI remains an initial interface.

**Deployment:** Deployment remains infrastructure-neutral. Local/OrbStack, generic Docker or systemd, and other supported environments are valid. OCI plus Cloudflare is an optional user-owned reference target, not a product dependency.

---

## Current state and factual progress

- Fork: `https://github.com/Vidanez/openjarvis_with_breaks`
- Local clone: `/Users/jvidanez/Documents/Repositories/openjarvis_with_breaks`
- `origin` is the personal fork; `upstream` tracks `open-jarvis/OpenJarvis` with push disabled.
- The fork has no own commits or `openjarvis_with_breaks` profile yet.
- OpenJarvis already contains model/engine configuration, tool and MCP support, approval primitives, connectors, memory/learning, an API server, sandbox support, and channels.
- OCI CLI authentication is resolved (`AUTH_OK`).
- OCI Always Free capacity remains blocked in Madrid: the observed capacity report has not admitted the previously considered shapes. The saved Resource Manager stack is reusable but does not reserve capacity.
- OrbStack `2.2.5` and Docker `29.8.2` are installed locally for optional local validation.

## Product boundary

1. Preserve upstream OpenJarvis model and engine behavior by default. Local Ollama and supported external providers remain ordinary options; no provider registry, mandatory admission record, region/retention approval, budget cap, or fail-closed metering is required merely to use a model.
2. Preserve upstream tool and MCP behavior as sufficient for now. Do not add a mandatory named-service registry, endpoint hashing, MCP admission flow, or special tool profile. Future hardening can be assessed independently.
3. Direct authenticated owner conversations may be learned automatically and may generate suggestions. Preferences remain attributable, reviewable, correctable, and erasable.
4. Email, documents, attachments, inbound messages, links, webhooks, and model output are untrusted input. They may generate clearly attributed proposals or suggestions for the owner, but cannot independently execute an external action or silently grant permissions.
5. An external effect means a send, write, delete, schedule, configuration change, or comparable mutation outside the assistant. It requires owner confirmation tied to the proposed effect. Ordinary conversation, learning, and suggestions do not require an effect confirmation.
6. Hermes is an optional future independent peer, not this active Hermes profile. A later interoperability design may define bounded messages between the two systems; this plan does not prescribe profile access, plugins, cost controls, or a final protocol.

## Delivery slices

### Slice 0 — Documentation contract

**Objective:** Establish the concise authority, learning, proposal, deployment, and future-peer contract.

**Files:**
- `docs/openjarvis-with-breaks/architecture.md`
- `docs/openjarvis-with-breaks/capability-matrix.md`
- `docs/openjarvis-with-breaks/operations.md`

**Work:**
1. Document upstream-compatible model/provider and tool/MCP behavior.
2. Define owner learning and proposal handling without treating ordinary suggestions as external effects.
3. Define the external-effect confirmation boundary.
4. Record OCI/Cloudflare only as an optional reference deployment and Hermes only as a future independent peer.

**Verification:** Markdown heading/fence/whitespace checks and `git diff --check`.

### Slice 1 — Trust boundary for external effects

**Objective:** Classify authenticated owner conversations and untrusted inbound/model content without replacing upstream model, tool, MCP, or engine selection behavior.

**Work:**
1. Carry provenance for direct owner conversation, external inbound content, and model output at relevant interaction boundaries.
2. Allow owner-originated learning and suggestions under the documented memory policy.
3. Present proposals derived from external inbound content or model output with clear attribution.
4. Require confirmation before any external effect; verify that untrusted content cannot cause one or silently grant permission.

**Acceptance:** Direct owner conversation can learn and suggest; untrusted content can propose but cannot autonomously act.

### Slice 2 — Owner confirmation for external effects

**Objective:** Add the smallest durable confirmation path for sends, writes, deletes, schedules, and comparable external mutations.

**Work:**
1. Show the owner an attributable proposal with the intended effect and target.
2. Execute only after owner confirmation for that effect.
3. Preserve ordinary upstream tool selection and normal conversations when no external effect is requested.
4. Add focused tests for denied untrusted effects, attributed proposals, and confirmed owner effects.

**Acceptance:** No inbound email/document/attachment/model output can autonomously execute an external action.

### Slice 3 — Memory and suggestions

**Objective:** Make owner learning useful and controllable without elevating external content to authority.

**Work:**
1. Preserve and use upstream memory/learning where compatible.
2. Attribute owner-learned preferences and provide review, correction, expiry, and deletion paths.
3. Let external content and model output create owner-visible, attributed suggestion candidates only.
4. Keep suggestions separate from execution authority.

**Acceptance:** Owner conversations may be learned automatically; external sources cannot silently create permissions or external effects.

### Slice 4 — Optional hardening assessment

**Objective:** Assess, rather than mandate, additional provider, tool, MCP, attachment, or sandbox hardening after the core experience works.

**Work:**
1. Evaluate optional provider preferences, cost observations, privacy choices, and operational limits as non-blocking enhancements.
2. Evaluate tool/MCP and attachment hardening against actual upstream behavior and user needs.
3. Do not redefine ordinary models, tools, MCP, or conversation as default-denied unless a later approved design explicitly chooses that behavior.

**Acceptance:** Any hardening proposal is documented as optional and does not block normal upstream functionality by default.

### Slice 5 — Deployment options and future peer interoperability

**Objective:** Validate supported deployment options and design future bounded peer messaging only when needed.

**Work:**
1. Validate locally with OrbStack or another supported local environment.
2. Support generic Docker, systemd, or other appropriate infrastructure without making OCI or Cloudflare prerequisites.
3. If the user selects the OCI/Cloudflare reference target, recheck capacity, cost, runtime fit, and owner authorization before provisioning.
4. Produce a separate future interoperability design before connecting OpenJarvis to an independent Hermes peer.

**Acceptance:** The product remains deployable without OCI/Cloudflare, and no Hermes-profile access or plugin is implied.

## Work-unit and review order

1. Slice 0 establishes the contract.
2. Slices 1–3 establish the concise authority, proposal, confirmation, and learning behavior.
3. Slice 4 is optional follow-up hardening, not an activation gate for upstream models or tools.
4. Slice 5 is optional deployment and interoperability work after the product behavior is verified.

## Overall validation

- Focused tests added by later implementation slices.
- A scenario matrix proves that untrusted email, document, attachment, inbound message, and model output can create attributed proposals but cannot autonomously execute external effects.
- A direct owner conversation can be learned and can create suggestions without an external-effect confirmation.
- Deployment smoke tests run in the selected supported environment; OCI is tested only if selected.
- Markdown heading/fence/whitespace checks and `git diff --check` for this documentation slice.

## Explicitly deferred

- Mandatory provider registries, admission records, cost caps, region/retention approvals, and fail-closed metering for normal model use.
- Mandatory named MCP/tool service registries, endpoint hashing, MCP admission, and special tool profiles.
- Attachment quarantine and other tool/MCP hardening beyond upstream safe defaults.
- OCI or Cloudflare as product requirements.
- A Hermes integration protocol, plugin installation, or access to any current Hermes profile.
