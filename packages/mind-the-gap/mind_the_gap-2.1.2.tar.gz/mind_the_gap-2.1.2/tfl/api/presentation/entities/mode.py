from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Mode:
    isTflService: bool
    isFarePaying: bool
    isScheduledService: bool
    modeName: bool
