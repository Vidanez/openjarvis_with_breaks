# Security test baseline

The fork runs `.github/workflows/security-sast.yml` on pull requests to `main` and pushes to `main`. It is a narrow source-level baseline; it does not change runtime behavior or authorize external services.

## PR policy

| Check | Policy |
| --- | --- |
| Gitleaks scan of commits in the pull request or push, including `.github/workflows/` changes | Blocking |
| Bandit findings with high severity and high confidence in `src/openjarvis` | Blocking |
| `pip-audit` known dependency advisories | Report-only until maintainers explicitly triage and change the policy |
| Semgrep `p/python` and `p/security-audit` findings | Report-only until maintainers explicitly triage and change the policy |

A tool execution failure that prevents the report from being produced is still a workflow failure. Report-only means findings are visible for review, not that an unavailable scanner is silently accepted.

## Safe local reproduction

Run these commands from the repository root. They inspect checked-out source and dependencies; they do not call application connectors, send messages, invoke OCI, start Hermes, or require provider credentials.

```bash
# Requires the Gitleaks CLI on PATH. Scan only commits introduced by the branch,
# matching the GitHub action's PR/push range rather than unrelated repository history.
first_commit="$(git rev-list --reverse origin/main..HEAD | head -n 1)"
test -n "$first_commit"
gitleaks git --redact --no-banner \
  --log-opts="--no-merges --first-parent ${first_commit}^..HEAD"

# Check uncommitted source and workflow changes before creating the commit.
git diff --binary -- src .github/workflows | gitleaks stdin --redact --no-banner

uv run --with bandit==1.9.4 bandit -r src/openjarvis -lll -iii -f screen

report_dir="${TMPDIR:-/tmp}/openjarvis-security"
mkdir -p "$report_dir"
uv export --locked --no-dev --no-emit-project --no-header > "$report_dir/requirements-core.txt"
uv run --with pip-audit==2.10.1 pip-audit -r "$report_dir/requirements-core.txt" \
  --disable-pip --require-hashes --strict --progress-spinner off \
  --format json --output "$report_dir/pip-audit-core.json" || true
semgrep --config=p/python --config=p/security-audit --error --skip-unknown-extensions src/openjarvis || true
```

The `|| true` commands preserve the workflow's report-only advisory policy. Review their output; do not convert them to blocking checks until advisory triage is explicit. GitHub runs the same secret scanner through `gitleaks/gitleaks-action@v2` on an Ubuntu runner.

## Security regression expectations

Changes that cross a security boundary need a focused, hermetic regression test in the same PR:

- **External effects:** prove refusal, confirmation, or allowlist behavior before network, subprocess, filesystem mutation, message delivery, or other effectful adapters are reached.
- **Authentication and authorization:** test missing, malformed, and unauthorized credentials at the public boundary; prove the allowed path uses the required identity and capability.
- **Connectors:** use fakes at the connector seam; assert credentials and untrusted payloads are not logged or forwarded outside the documented request contract.
- **Untrusted messages:** test hostile prompt, webhook, channel, or tool input through the boundary; assert validation, sanitization, or blocking occurs before it reaches privileged instructions or effectful tools.

Keep these tests local and deterministic. Do not use live credentials, provider accounts, OCI, Hermes, or real connectors as regression-test fixtures.
