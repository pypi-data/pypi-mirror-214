from typing import Optional

import pkg_resources
import requests

_PYPI_URL = "https://pypi.org/pypi/elementary-data/json"


def get_package_version() -> Optional[str]:
    try:
        return pkg_resources.get_distribution("elementary-data").version
    except Exception:
        return None


def get_latest_package_version() -> Optional[str]:
    try:
        resp = requests.get(_PYPI_URL)
        resp.raise_for_status()
        return resp.json().get("info", {}).get("version")
    except Exception:
        return None
