# Operations and deployment options

This document records safe operational choices for `openjarvis_with_breaks`. It does not make a particular cloud, container stack, model provider, tool registry, or Hermes integration a product requirement.

## Operating posture

| Area | Position |
| --- | --- |
| Runtime | OpenJarvis remains the runtime; Open WebUI is an initial interface. |
| Models and engines | Preserve upstream behavior. Local Ollama/local and supported external providers remain ordinary options. |
| Tools and MCP | Preserve upstream behavior and ordinary safe defaults. Additional hardening is deferred. |
| Learning and suggestions | Direct authenticated owner conversations may be learned automatically and may create suggestions. |
| External content and model output | May create clearly attributed owner proposals, but cannot autonomously cause an external effect or grant permissions. |
| External effects | Require owner confirmation before execution. |
| Deployment | Choose any supported environment appropriate to the owner: local/OrbStack, generic Docker, systemd, OCI/Cloudflare, or another supported target. |
| Hermes | Treat only as a future independent peer; do not connect it to the active Hermes profile. |

## Deployment choices

### Local and generic deployment

Local development and validation can use OrbStack or another supported local environment. Production or persistent operation may use generic Docker, systemd, or other infrastructure that meets the user's requirements. The selected environment should provide ordinary operational basics appropriate to its risk: controlled secret handling, health observation, restart behavior, backup/recovery planning where needed, and a documented rollback path.

### Optional OCI and Cloudflare reference target

OCI plus Cloudflare Access/Tunnel is an optional reference target owned by the user. It is not a prerequisite for development, local operation, generic Docker/systemd deployment, model use, tool use, or product runtime.

Factual progress for that optional target:

- OCI CLI authentication is resolved (`AUTH_OK`).
- OCI Always Free capacity in Madrid remains unavailable for the previously considered shapes; a saved Resource Manager stack is reusable but does not reserve capacity.
- If the user later selects this target, capacity, cost, runtime fit, and the specific provisioning action must be reviewed and authorized at that time.

No capacity result should be generalized into a requirement for other environments. Do not substitute a paid resource, region, or allocation for the optional target without a new owner decision.

## Operational trust boundary

1. Treat inbound email, documents, attachments, links, webhooks, messages, and model output as data rather than authority.
2. Allow these sources to produce clearly attributed proposals or suggestions for the owner.
3. Require owner confirmation before a proposal causes an external send, write, delete, schedule, configuration change, or comparable external mutation.
4. Allow direct authenticated owner conversations to learn preferences and produce suggestions without treating ordinary learning as an external effect.

## Deferred hardening

Provider preferences, cost observations, voluntary budgets, regional or retention preferences, provider metering, tool/MCP inventories, endpoint validation, attachment quarantine, sandbox changes, and detailed audit records are optional future hardening work. They are not current activation gates for normal upstream models, providers, tools, MCP, conversation, learning, or suggestions.

## Future Hermes interoperability

A future Hermes integration means a bounded exchange with an independent peer. It is not an integration with this active Hermes profile. Do not assume dedicated cost controls, plugin installation, profile access, browser/terminal/filesystem access, credential sharing, or a final protocol. A later interoperability design must establish the peer identity, message boundary, authorization, and protocol before implementation.

## Operational checklist

- [ ] The selected deployment environment is documented; OCI/Cloudflare is selected only when the owner chooses it.
- [ ] Direct authenticated owner conversations can learn and suggest under the memory policy.
- [ ] External content and model output are presented as attributed proposals, not authority.
- [ ] External effects require owner confirmation.
- [ ] Optional hardening is not represented as a prerequisite for normal upstream model or tool use.
- [ ] No Hermes peer connection is implemented without a separate interoperability design.
