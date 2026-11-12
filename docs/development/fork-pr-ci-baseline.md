# Fork PR CI baseline

The fork's fast pull-request gate uses Python 3.12, Rust stable, uv 0.12.19, and the committed `uv.lock`. It builds the mandatory `openjarvis_rust` extension before linting and hermetic Python tests in `tests/core`, `tests/security`, and `tests/deploy`. The upstream CI and SAST workflows remain the comprehensive Rust workspace, Windows, coverage, and security gates.

Run the same checks locally from the repository root:

```bash
uv sync --locked --extra dev --extra server --python 3.12
uv run maturin develop --manifest-path rust/crates/openjarvis-python/Cargo.toml
uv run ruff check src/ tests/
uv run ruff format --check src/ tests/
uv run pytest tests/core tests/security tests/deploy -q --tb=short \
  -m "not live and not cloud and not hub and not live_channel and not live_external and not docker and not modal"
```

The marker expression prevents tests that require running services, cloud credentials, Hugging Face downloads, external framework processes, Docker, or Modal. This gate builds only the Python extension binding; it does not run Rust workspace tests, Windows tests, download models, or invoke OCI, Hermes, or connector services.
