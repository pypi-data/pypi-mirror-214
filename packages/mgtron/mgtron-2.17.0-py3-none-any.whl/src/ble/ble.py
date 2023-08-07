"""Make the API calls directly to the Rust API."""

import requests
import logging

loggei = logging.getLogger(name=__name__)


def ble_rs(target: str) -> dict:
    """Call the BLE RS API and return the data."""
    loggei.debug(msg=f"{ble_rs.__name__}()")

    port = 8080

    try:
        data = requests.get(
            url=f"http://localhost:{port}/{target}",
            headers={"Content-Type": "application/json"},
        )

        if data.status_code != 200:
            loggei.error(msg=f"BLE API returned {data.status_code}")
            return {}

        loggei.info(msg=f"BLE API raw response: {data}")

        data: dict = data.json()

        return data

    except requests.exceptions.ConnectionError as e:
        loggei.error(msg=f"BLE API not running: {e}")
        return {"Status": requests.status_codes}
