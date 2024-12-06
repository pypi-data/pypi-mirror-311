from typing import List

import requests

from tfl import BASE_URL
from tfl.api.factory import from_json
from tfl.api.presentation.entities.mode import Mode
from tfl.api.presentation.entities.status_severity import StatusSeverity

ENDPOINT = f"{BASE_URL}/Line/Meta"


def modes() -> List[Mode]:
    json = requests.get(f"{ENDPOINT}/Modes").json()
    return from_json(json)


def severity() -> List[StatusSeverity]:
    json = requests.get(f"{ENDPOINT}/Severity").json()
    return from_json(json)


def disruption_categories() -> List[str]:
    json = requests.get(f"{ENDPOINT}/DisruptionCategories").json()
    return json


def service_types() -> List[str]:
    json = requests.get(f"{ENDPOINT}/ServiceTypes").json()
    return json
