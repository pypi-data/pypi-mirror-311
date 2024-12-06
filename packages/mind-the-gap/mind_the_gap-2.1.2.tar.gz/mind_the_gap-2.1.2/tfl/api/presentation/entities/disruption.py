from __future__ import annotations

from dataclasses import dataclass
from typing import List

from tfl.api.presentation.entities.additional_properties import AdditionalProperties


@dataclass
class Crowding:
    pass


@dataclass
class LineGroup:
    stationAtcoCode: str
    lineIdentifier: List[str]


@dataclass
class LineModeGroup:
    modeName: str
    lineIdentifier: List[str]


@dataclass
class Identifier:
    id: str
    name: str
    uri: str
    type: str
    crowding: Crowding
    routeType: str
    status: str


@dataclass
class RouteSection:
    id: str
    lineId: str
    routeCode: str
    name: str
    lineString: str
    direction: str
    originationName: str
    destinationName: str
    validTo: str
    validFrom: str
    routeSectionNaptanEntrySequence: List[RouteSectionNaptanEntrySequence]
    pass


@dataclass
class StopPoint:
    naptanId: str
    platformName: str
    indicator: str
    stopLetter: str
    modes: List[str]
    icsCode: str
    smsCode: str
    stopType: str
    stationNaptan: str
    accessibilitySummary: str
    hubNaptanCode: str
    lines: List[Identifier]
    linesGroup: List[LineGroup]
    lineModeGroups: List[LineModeGroup]
    fullName: str
    naptanMode: str
    status: bool
    id: str
    url: str
    commonName: str
    distance: float
    placeType: str
    additionalProperties: List[AdditionalProperties]
    children: List[StopPoint]
    childrenUrl: List[str]
    lat: float
    lon: float


@dataclass
class RouteSectionNaptanEntrySequence:
    ordinal: int
    stopPoint: StopPoint


@dataclass
class Disruption:
    category: str
    type: str
    categoryDescription: str
    description: str
    created: str
    lastUpdate: str
    affectedRoutes: List[RouteSection]
    affectedStops: List[StopPoint]
    closureText: str
