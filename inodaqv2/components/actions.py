from math import ceil
from typing import TypedDict
from inoio import errors
from inodaqv2.components.extensions import conn

ANALOG_TO_VOLT = 5.0 / 1023
DUTY_CYCLE_TO_ANALOG = 255 / 100
TYPE_PAYLOAD_DIG = TypedDict(
    "TYPE_PAYLOAD_DIG",
    {
        "rv": bool,
        "message": str,
    },
)
TYPE_PAYLOAD_AREAD = TypedDict(
    "TYPE_PAYLOAD_AREAD",
    {
        "rv": bool,
        "message": str,
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
        "message": str,
        "A0": int,
        "A1": int,
        "A2": int,
        "A3": int,
        "A4": int,
        "A5": int,
    },
)
TYPE_PAYLOAD_PWM = TypedDict(
    "TYPE_PAYLOAD_PWM",
    {
        "rv": bool,
        "message": str,
    },
)


def toggle_digital_pins(pin: str, state: bool) -> TYPE_PAYLOAD_DIG:
    pin_id = pin.split("-")[1]

    command = f"dig:{pin_id}:"

    if state:
        command += "on"
    else:
        command += "off"

    try:
        conn.write(command)
    except errors.InoIOTransmissionError as e:
        return {
            "rv": False,
            "message": str(e),
        }

    return {
        "rv": True,
        "message": conn.read(),
    }


def read_analog_pins() -> TYPE_PAYLOAD_AREAD:
    try:
        conn.write("aread")
    except errors.InoIOTransmissionError as e:
        return {
            "rv": False,
            "message": str(e),
            "A0": -1.00,
            "A1": -1.00,
            "A2": -1.00,
            "A3": -1.00,
            "A4": -1.00,
            "A5": -1.00,
        }

    message = conn.read()

    _, values = message.split(";")
    volts = values.split(",")

    return {
        "rv": True,
        "message": message,
        "A0": round(int(volts[0]) * ANALOG_TO_VOLT, 3),
        "A1": round(int(volts[1]) * ANALOG_TO_VOLT, 3),
        "A2": round(int(volts[2]) * ANALOG_TO_VOLT, 3),
        "A3": round(int(volts[3]) * ANALOG_TO_VOLT, 3),
        "A4": round(int(volts[4]) * ANALOG_TO_VOLT, 3),
        "A5": round(int(volts[5]) * ANALOG_TO_VOLT, 3),
    }


def read_digital_pins() -> TYPE_PAYLOAD_DREAD:
    try:
        conn.write("dread")
    except errors.InoIOTransmissionError as e:
        return {
            "rv": False,
            "message": str(e),
            "A0": -1,
            "A1": -1,
            "A2": -1,
            "A3": -1,
            "A4": -1,
            "A5": -1,
        }

    message = conn.read()

    _, values = message.split(";")
    volts = values.split(",")

    return {
        "rv": True,
        "message": message,
        "A0": int(volts[0]),
        "A1": int(volts[1]),
        "A2": int(volts[2]),
        "A3": int(volts[3]),
        "A4": int(volts[4]),
        "A5": int(volts[5]),
    }


def set_pwm(pin: str, value: str) -> TYPE_PAYLOAD_PWM:
    pin_id = pin.split("-")[1]

    pwm = ceil(int(value) * DUTY_CYCLE_TO_ANALOG)
    command = f"pwm:{pin_id}:{pwm}"

    try:
        conn.write(command)
    except errors.InoIOTransmissionError as e:
        return {
            "rv": False,
            "message": str(e),
        }

    return {"rv": True, "message": conn.read()}
