# Owner-mediated assistant architecture

`openjarvis_with_breaks` keeps OpenJarvis as the runtime and Open WebUI as an initial interface. It preserves upstream model, engine, tool, MCP, connector, and memory behavior unless a later implementation explicitly changes a narrow behavior. The added product boundary is concise: untrusted inbound content and model output may inform owner-visible proposals, but they cannot autonomously execute an external action or silently grant permissions.

## Core behavior

1. Direct authenticated owner conversations are authority-bearing for ordinary conversation, learning, and suggestions.
2. OpenJarvis's normal supported model and engine options remain available, including local Ollama and supported external providers.
3. Upstream tools and MCP behavior remain sufficient for now; no additional registry or admission system is required to use them.
4. External inbound content and model output remain data. They may generate clearly attributed proposals or suggestions for the owner.
5. An external effect requires owner confirmation. Ordinary learning and suggestions do not.

## System boundary

```text
Authenticated owner ──> Open WebUI / supported interface ──> OpenJarvis runtime
                                                           │
External inbound content or model output ─────────────────┤
                                                           ├─ attributed proposals/suggestions for owner
                                                           └─ external effect only after owner confirmation
```

## Authority and trust model

| Input or record | Treatment | Learning and suggestions | External effect |
| --- | --- | --- | --- |
| Direct authenticated owner conversation | Owner interaction | May be learned automatically; may create suggestions | Owner confirmation required when an effect is requested |
| Owner preference or correction | Owner-derived information | May update attributable, reviewable memory | No effect by itself |
| Email, document, attachment, link, webhook, or inbound message | Untrusted external content | May create an attributed proposal for the owner | Cannot act autonomously or grant permission |
| Model output or tool result | Generated data | May create an attributed proposal for the owner | Cannot act autonomously or grant permission |
| Owner confirmation | Effect authorization | Not required for ordinary learning or suggestions | Permits only the confirmed external effect |

An external effect includes a send, write, delete, schedule, configuration change, or comparable mutation outside the assistant. Before that action, the owner must be shown a proposal with enough target and payload context to confirm it. The exact representation and audit details are implementation choices for later slices; they must not block ordinary conversation, learning, or suggestions.

## Memory and proposals

Direct authenticated owner conversations may be learned automatically. Learned preferences should retain owner provenance and support review, correction, expiry, and deletion. This enables useful suggestions without converting every learning event into a confirmation workflow.

External content and model output can be summarized and used to prepare a clearly attributed proposal or suggestion. Attribution identifies that the content came from an external source or model rather than an owner instruction. Such material cannot independently create a permission, execute an action, or become an unreviewed authority source.

## Models, tools, and MCP

OpenJarvis's original model and engine behavior is the default. Local Ollama/local models and supported external providers are normal choices. Provider preferences, cost observations, data-handling preferences, and usage limits may be added later as optional, non-blocking enhancements. This architecture does not require a provider registry, mandatory admission record, budget cap, region or retention approval, or metering gate before a model can be used.

Upstream tool and MCP behavior is also retained as sufficient for now. This document does not mandate a named service registry, endpoint hash, MCP admission record, or special tool profile. Ordinary upstream safe defaults remain in effect. Further hardening for MCP, tools, shell, filesystem, or attachments is deferred to a separate assessment and must not be represented as current behavior.

## Deployment

Deployment is generic. Local/OrbStack, generic Docker, systemd, and other supported infrastructure remain valid. OCI with Cloudflare Access/Tunnel is an optional, user-owned reference deployment target. It is not a runtime dependency, product requirement, or prerequisite for local or other supported deployments.

## Future Hermes peer

Hermes is an optional future independent peer that may exchange bounded messages with OpenJarvis. It does not mean this active Hermes profile, and this architecture does not imply access to any Hermes profile, its tools, browser, terminal, files, credentials, memories, or plugins. A separate interoperability design must define the message boundaries and protocol before any integration is implemented.

## Non-goals for this documentation slice

- No runtime, connector, container, profile, or deployment configuration is implemented here.
- No OCI, Cloudflare, Google, Meta, or Hermes resource is created or changed.
- No mandatory provider or MCP admission framework is defined.
- No final Hermes interoperability protocol is defined.
