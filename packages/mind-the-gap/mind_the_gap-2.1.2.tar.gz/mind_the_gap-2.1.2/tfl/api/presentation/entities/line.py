from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from tfl.api.presentation.entities.disruption import Crowding, Disruption


@dataclass
class LineServiceTypeInfo:
    name: str
    uri: str


@dataclass
class ValidityPeriod:
    fromDate: str
    toDate: str
    isNow: bool
    pass


@dataclass
class LineStatus:
    id: int
    statusSeverity: int
    statusSeverityDescription: str
    created: str
    validityPeriods: List[ValidityPeriod]
    disruption: Optional[Disruption] = None


@dataclass
class Line:
    id: str
    name: str
    modeName: str
    disruption: List[Disruption]
    created: str
    modified: str
    lineStatuses: List[LineStatus]
    # routeSections: []
    serviceTypes: List[LineServiceTypeInfo]
    crowding: Optional[Crowding] = None
