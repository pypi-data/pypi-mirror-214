"""Process the BLE data."""

import dearpygui.dearpygui as dpg
import time
from src.ble.helpers import ThreadWithReturnValue
from src.ble.ble import ble_rs
import logging

loggei = logging.getLogger(name=__name__)


def ble_data(company: bool) -> list:
    """Collate the da from the BLE API and return it."""
    loggei.debug(msg=f"{ble_data.__name__}()")

    target: tuple[str, str] = "rssi", "company"

    # Grab the data from the API
    data = ble_rs(
        target=target[0]
    ) if not company else ble_rs(
        target=target[1]
    )

    loggei.info(msg=data)

    # If the data is empty, return an empty dict
    if not data:
        return {}

    # Grab the data from the dict
    if not company:
        macs, rssi = (data.keys(), data.values())

    else:
        macs, companies = (data.keys(), data.values())

    return [
        list(macs),
        list(rssi)
    ] if not company else [
        list(macs),
        list(companies)
    ]


def ble_data_complete() -> list[tuple[str, tuple[str, str]]]:
    """Get the MAC address, Manufacturer, and RSSI."""
    company = True, False

    dpg.add_text(
        tag="scan_text",
        default_value="Scanning"
    )

    dpg.add_text(
        tag="scan_text_",
        default_value='-' * 78
    )

    ble = ThreadWithReturnValue(
        target=ble_data,
        args=(company[0],)
    )
    ble.start()

    ble_rssi = ThreadWithReturnValue(
        target=ble_data,
        args=(company[1],)
    )

    for i in range(1, 5):
        time.sleep(1)
        dpg.configure_item(
            item="scan_text",
            default_value="Scanning" + "." * i
        )

    ble_rssi.start()

    ble = ble.join()
    ble_rssi = ble_rssi.join()

    dpg.delete_item(item="scan_text")
    dpg.delete_item(item="scan_text_")

    if ble[0][0] == "Status":
        loggei.error(msg="BLE API not running")
        ble = [("status", ("BLE API not running", "BLE API not running"))]
        return ble

    ble.insert(3, [])

    loggei.info(f"ble_company length: {len(ble[0])}")
    loggei.info(f"ble_rssi length: {len(ble_rssi[0])}")

    try:
        for i, mac in enumerate(ble_rssi[0]):
            mac = mac.split(']')[1]
            for mac_2 in ble[0]:
                if mac_2 == mac:
                    ble[2].insert(i, int(ble_rssi[-1][i]))
                    break
    except IndexError as e:
        loggei.warning(msg=f"BLE fail: {e}")

    for i in range(len(ble)):

        if len(ble[0]) != len(ble[2]):
            loggei.warn(msg="ble[0] != ble[2]")
            loggei.debug(msg=f"ble after insert: {ble}")

    ble = dict(zip(ble[0], zip(ble[1], ble[2])))

    ble = sorted(ble.items(), key=lambda x: x[1][1], reverse=True)

    return ble
