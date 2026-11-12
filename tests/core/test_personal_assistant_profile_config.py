"""Tests for loading the fail-closed personal assistant profile."""

from __future__ import annotations

from pathlib import Path

import pytest

from openjarvis.core.config import load_config


def test_load_config_applies_personal_assistant_profile(tmp_path: Path) -> None:
    config_path = tmp_path / "config.toml"
    config_path.write_text(
        "[profile]\n"
        "uploads = true\n"
        "automatic_external_effects = true\n"
        'automation_admission = "approved-workflow"\n',
        encoding="utf-8",
    )

    config = load_config(config_path)

    assert config.profile.uploads is True
    assert config.profile.automatic_external_effects is True
    assert config.profile.automation_admission == "approved-workflow"


def test_load_config_rejects_unadmitted_automatic_external_effects(
    tmp_path: Path,
) -> None:
    config_path = tmp_path / "config.toml"
    config_path.write_text(
        "[profile]\n"
        "automatic_external_effects = true\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="automatic_external_effects requires automation_admission",
    ):
        load_config(config_path)
