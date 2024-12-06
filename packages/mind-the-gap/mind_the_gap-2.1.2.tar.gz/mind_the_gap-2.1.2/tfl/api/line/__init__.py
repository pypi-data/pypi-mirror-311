from typing import Tuple

import requests

from tfl import BASE_URL
from tfl.api.factory import from_json

ENDPOINT = f"{BASE_URL}/Line"


def by_id(*ids: Tuple[str, ...], status=False):
    line_ids = ",".join(ids)
    endpoint = f"{ENDPOINT}/{line_ids}" + ("/Status" if status else "")
    json = requests.get(endpoint).json()
    return from_json(json)


def by_mode(mode: str):
    json = requests.get(f"{ENDPOINT}/Mode/{mode}").json()
    return from_json(json)
