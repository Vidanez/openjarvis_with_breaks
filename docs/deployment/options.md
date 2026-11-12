---
title: Deployment options
summary: Choose a small, user-owned deployment for a personal OpenJarvis assistant.
---

# Deployment options

OpenJarvis is a personal assistant core intended to stay available for its owner.
Choose the smallest deployment that provides the uptime, storage, and network
boundary you need. Docker, systemd, and OCI are operational choices; none is a
product dependency.

## Choose a path

| Need | Recommended path | When to use it |
| --- | --- | --- |
| Local development or a quick container check | [Local OrbStack smoke test](docker.md#local-orbstack-smoke-test) | macOS local validation only; it is not a production configuration. |
| One always-on machine with containers | [Docker Compose](docker.md) | Keep the API and an optional local inference engine together. |
| One always-on Linux machine without containers | [systemd](systemd.md) | Use the supplied service unit and an engine reachable from that host. |
| A user-owned cloud VM | Generic Docker or systemd | Apply the same host, storage, secret, health, and rollback checks as for any Linux host. |
| OCI plus an existing Cloudflare-managed domain | [OCI reference path](#oci-reference-path-optional) | A worked operational target, not a required service or supported control plane. |

For the HTTP server and reverse-proxy boundary, see the [API server guide](api-server.md).
For macOS background execution without containers, see [launchd](launchd.md).

## Baseline for a 24/7 personal assistant

Before choosing a target, decide these owner-controlled details:

- **Availability:** a host that remains powered and connected when the assistant
  should be reachable.
- **State:** durable storage and backups for the data the owner elects to keep,
  such as configuration, memory, telemetry, and traces. Do not treat an
  ephemeral container filesystem as durable state.
- **Network boundary:** bind the API to loopback when a reverse proxy is used;
  otherwise restrict the host firewall to the clients that need access.
- **Authentication:** an API key is required when `jarvis serve` binds to a
  non-loopback address. Generate it with `jarvis auth generate-key` and send it
  as a bearer token to protected API routes.
- **Inference:** run a local engine on the host, run it as a container, or
  configure a provider the owner has chosen. The deployment target does not
  dictate an inference provider.

## Target checklist

Use this checklist for every target before calling it an always-on deployment.

| Check | What to verify |
| --- | --- |
| Health | `curl --fail http://<host>:<port>/health` returns HTTP 200 from the intended network boundary. |
| Restart | Reboot or restart the service and confirm the supervisor (`docker compose` restart policy, systemd, or launchd) brings it back. |
| Persistent state | The selected data path is on durable storage and its backup/restore procedure has been tested. |
| Secrets | Store API keys and provider credentials outside the image and repository: a protected environment file, a service secret store, or the platform's secret facility. Do not put them in Compose files, unit files committed to git, command history, or screenshots. |
| Exposure | Confirm only the expected ports are published and TLS/reverse-proxy configuration is owned and tested where remote access is required. |
| Rollback | Keep the prior image reference or application revision and the previous configuration. Revert the reference, restart the service, and repeat the health check. |

## Generic Docker path

Use the repository Compose configuration as the portable container baseline:

```bash
cd deploy/docker
cp .env.example .env
# Set OPENJARVIS_API_KEY in .env without committing the file.
docker compose up -d
docker compose ps
curl --fail http://127.0.0.1:8000/health
```

The included Compose file starts OpenJarvis and Ollama. For a different
inference topology, build from the supplied Dockerfile and configure the
server's engine and model for the service you operate. Pin image references
that matter to your rollback process, and mount any state that must survive
container replacement. See [Docker deployment](docker.md) for CPU/GPU variants,
health checks, and configuration mounts.

To roll back a Compose deployment, restore the previous image/configuration
reference, run `docker compose up -d`, then repeat the health check. Do not use
`docker compose down --volumes` unless deleting local state is intentional.

## Generic systemd path

For a non-container Linux host, install OpenJarvis under a dedicated service
account and use the supplied `deploy/systemd/openjarvis.service` as a starting
point. Create its protected environment file before starting the unit, then
use `systemctl` and `journalctl` for lifecycle and logs. The [systemd guide](systemd.md)
covers the exact unit, API-key file, configuration location, and recovery
commands.

A systemd rollback is a controlled application/configuration rollback: restore
the previous release or virtual environment, reload the unit if it changed,
restart it, and verify `/health`.

## OCI reference path (optional)

OCI is one example of a user-owned Linux VM target. It is not required to run
OpenJarvis, and the project does not provision, configure, or depend on OCI or
Cloudflare.

Treat OCI capacity as a **reference-target constraint**: before committing to
this path, the owner must confirm that the selected region and instance shape
are available, have enough CPU, memory, disk, and network capacity for the
chosen model/engine, and fit the owner's cost and uptime requirements. If that
capacity is unavailable, choose another host or deployment path; OpenJarvis
itself does not block on it.

A minimal owner-operated path is:

1. Create or select an OCI Linux VM and durable block storage under the owner's
   account.
2. Apply normal host maintenance and a least-exposure firewall policy before
   installing OpenJarvis.
3. Install Docker Compose or systemd, then follow the matching generic path
   above. Keep persistent OpenJarvis data on the selected durable storage.
4. Verify `/health` locally first. Expose the service only through an
   owner-managed TLS/reverse-proxy boundary when remote access is required.
5. If the owner already uses Cloudflare for a domain, they may route that
   boundary through their existing Cloudflare configuration. Cloudflare is
   optional: no DNS record, tunnel, token, or dashboard change is assumed by
   this project.

For rollback, retain the former VM image/application revision and the previous
reverse-proxy configuration. Restore the previous version, restart the service,
and perform the same local and externally intended health checks. OCI and
Cloudflare changes remain the owner's operational responsibility.
