from __future__ import annotations

from dataclasses import dataclass


@dataclass
class StatusSeverity:
    modeName: str
    severityLevel: int
    description: str
