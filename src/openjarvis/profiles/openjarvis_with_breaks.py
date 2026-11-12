"""Fail-closed capability profile for the personal assistant."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PersonalAssistantProfile:
    """Explicitly admit assistant capabilities; deny them by default."""

    uploads: bool = False
    google_mutation: bool = False
    baileys: bool = False
    mcp: bool = False
    shell: bool = False
    filesystem: bool = False
    cloud_providers: bool = False
    automatic_external_effects: bool = False
    automation_admission: str = ""

    def validate(self) -> None:
        """Reject automatic external effects without an explicit admission."""
        if self.automatic_external_effects and not self.automation_admission:
            raise ValueError("automatic_external_effects requires automation_admission")
