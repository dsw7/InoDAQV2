from typing import TypedDict, Optional
from inoio import errors
from inodaqv2.components.extensions import conn

ANALOG_TO_VOLT = 5.0 / 1023
TYPE_PAYLOAD_DIG = TypedDict(
    "TYPE_PAYLOAD_DIG",
    {
        "rv": bool,
        "message": Optional[str],
    },
)
TYPE_PAYLOAD_AREAD = TypedDict(
    "TYPE_PAYLOAD_AREAD",
    {
        "rv": bool,
        "message": Optional[str],
        "A0": float,
        "A1": float,
        "A2": float,
        "A3": float,
        "A4": float,
        "A5": float,
    },
)
TYPE_PAYLOAD_DREAD = TypedDict(
    "TYPE_PAYLOAD_DREAD",
    {
        "rv": bool,
        "message": Optional[str],
        "A0": int,
        "A1": int,
        "A2": int,
        "A3": int,
        "A4": int,
        "A5": int,
    },
)


def toggle_digital_pins(pin: str, state: bool) -> TYPE_PAYLOAD_DIG:
    pin_id = pin.split("-")[1]

    command = f"dig:{pin_id}:"

    if state:
        command += "on"
    else:
        command += "off"

    payload: TYPE_PAYLOAD_DIG = {"rv": True, "message": None}
    try:
        conn.write(command)
    except errors.InoIOTransmissionError as e:
        payload["rv"] = False
        payload["message"] = str(e)

    conn.read()  # Flush input buffer
    return payload


def read_analog_pins() -> TYPE_PAYLOAD_AREAD:
    payload: TYPE_PAYLOAD_AREAD = {
        "rv": True,
        "message": None,
        "A0": -1.00,
        "A1": -1.00,
        "A2": -1.00,
        "A3": -1.00,
        "A4": -1.00,
        "A5": -1.00,
    }

    try:
        conn.write("aread")
    except errors.InoIOTransmissionError as e:
        payload["rv"] = False
        payload["message"] = str(e)
        return payload

    _, values = conn.read().split(";")
    volts = values.split(",")

    payload["A0"] = round(int(volts[0]) * ANALOG_TO_VOLT, 3)
    payload["A1"] = round(int(volts[1]) * ANALOG_TO_VOLT, 3)
    payload["A2"] = round(int(volts[2]) * ANALOG_TO_VOLT, 3)
    payload["A3"] = round(int(volts[3]) * ANALOG_TO_VOLT, 3)
    payload["A4"] = round(int(volts[4]) * ANALOG_TO_VOLT, 3)
    payload["A5"] = round(int(volts[5]) * ANALOG_TO_VOLT, 3)

    return payload


def read_digital_pins() -> TYPE_PAYLOAD_DREAD:
    payload: TYPE_PAYLOAD_DREAD = {
        "rv": True,
        "message": None,
        "A0": -1,
        "A1": -1,
        "A2": -1,
        "A3": -1,
        "A4": -1,
        "A5": -1,
    }

    try:
        conn.write("dread")
    except errors.InoIOTransmissionError as e:
        payload["rv"] = False
        payload["message"] = str(e)
        return payload

    _, values = conn.read().split(";")
    volts = values.split(",")

    payload["A0"] = int(volts[0])
    payload["A1"] = int(volts[1])
    payload["A2"] = int(volts[2])
    payload["A3"] = int(volts[3])
    payload["A4"] = int(volts[4])
    payload["A5"] = int(volts[5])

    return payload
