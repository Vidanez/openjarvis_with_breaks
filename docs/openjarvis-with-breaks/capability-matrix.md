# Capability and authority matrix

This matrix describes the target product boundary for `openjarvis_with_breaks`. It preserves the upstream OpenJarvis model, engine, tool, and MCP defaults. It does not enable, disable, or replace upstream features by itself.

## Baseline

| Area | Contract |
| --- | --- |
| Models and engines | Preserve normal upstream selection and behavior. Local Ollama/local models and supported external providers remain normal options. |
| Tools and MCP | Preserve upstream behavior and ordinary safe defaults. Additional service registries, endpoint hashes, admission records, and special profiles are deferred hardening, not prerequisites. |
| Owner conversations | Direct authenticated owner conversations may be learned automatically and may produce suggestions. |
| External content and model output | May produce clearly attributed proposals or suggestions for the owner; cannot independently execute an external effect or silently grant permission. |
| External effects | Sends, writes, deletes, schedules, configuration changes, and comparable external mutations require owner confirmation. |
| Deployment | Local/OrbStack, generic Docker, systemd, OCI/Cloudflare, and other supported infrastructure are deployment choices; OCI/Cloudflare is optional. |
| Hermes | Optional future independent peer only. No current-profile access, plugin installation, cost control, or final protocol is implied. |

## Capability matrix

| Capability | Current product position | Owner interaction rule | Deferred or optional work |
| --- | --- | --- | --- |
| Local models, including Ollama | Normal upstream option | Use follows normal authenticated owner interaction | Optional performance and cost observations |
| Supported external model providers | Normal upstream option | Use follows normal authenticated owner interaction | Optional provider preferences, cost observations, data-handling choices, and limits |
| Upstream tools | Retained | An external effect requested through a tool requires owner confirmation | Optional tool hardening after a separate assessment |
| Upstream MCP | Retained | An external effect requested through MCP requires owner confirmation | Optional registry, endpoint validation, or service profiling if later justified |
| Direct owner learning | Enabled target behavior | No effect confirmation required for ordinary learning or suggestions | Review, correction, expiry, and deletion UX |
| External inbound content | Proposal source only | Owner reviews any proposal before confirming an external effect | Source-specific parsing and attachment safety assessment |
| Model output | Proposal source only | Owner reviews any proposal before confirming an external effect | Output provenance presentation improvements |
| Email, document, attachment, link, webhook, or message | Untrusted input | Cannot autonomously act or grant permission | Attachment and connector hardening assessment |
| Google or other connectors | Preserve upstream behavior pending later implementation | Owner confirmation required for external mutations | Narrower scopes or additional controls only if later selected |
| OCI/Cloudflare reference deployment | Optional user-owned target | Separate owner authorization before provisioning or configuration | Capacity, cost, and runtime-fit review when selected |
| Hermes peer messaging | Future option | Requires a later interoperability design | Bounded-message protocol and peer authorization design |

## External-effect confirmation boundary

The confirmation boundary applies only to external effects. It does not apply to ordinary conversation, owner preference learning, memory review, or owner-visible suggestions. A proposal generated from an external source or model must remain attributed to that source and must not become permission or execution authority by itself.

## Optional future enhancements

The following are useful candidates but are explicitly non-blocking: provider preferences; cost observations or voluntary budgets; regional or retention preferences; usage metering; MCP/tool service inventories; endpoint validation; attachment quarantine; sandbox improvements; and more detailed effect receipts. Any future enhancement must preserve the baseline that normal upstream model and tool behavior is not default-denied by this document.
