from dataclasses import FrozenInstanceError

import pytest

from openjarvis.profiles.openjarvis_with_breaks import PersonalAssistantProfile


def test_profile_defaults_deny_all_capabilities_and_is_immutable() -> None:
    profile = PersonalAssistantProfile()

    assert profile.uploads is False
    assert profile.google_mutation is False
    assert profile.baileys is False
    assert profile.mcp is False
    assert profile.shell is False
    assert profile.filesystem is False
    assert profile.cloud_providers is False
    assert profile.automatic_external_effects is False

    with pytest.raises(FrozenInstanceError):
        profile.uploads = True


def test_automatic_external_effects_require_automation_admission() -> None:
    profile = PersonalAssistantProfile(automatic_external_effects=True)

    with pytest.raises(ValueError, match="automation_admission"):
        profile.validate()
