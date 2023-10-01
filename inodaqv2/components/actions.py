from logging import getLogger
from math import ceil
from typing import TypedDict
from inoio import errors
from inodaqv2.components.extensions import conn

LOGGER = getLogger("inodaqv2")
ANALOG_TO_VOLT = 5.0 / 1023
DUTY_CYCLE_TO_ANALOG = 255 / 100

TYPE_PAYLOAD_AREAD = TypedDict(
    "TYPE_PAYLOAD_AREAD",
    {
        "rv": bool,
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
        "A0": int,
        "A1": int,
        "A2": int,
        "A3": int,
        "A4": int,
        "A5": int,
    },
)


def run_handshake() -> None:
    LOGGER.info("Handshaking with device")
    LOGGER.info('Sending command: "hello"')

    try:
        conn.write("hello")
    except errors.InoIOTransmissionError as e:
        LOGGER.exception("Failed to send command")
        raise ConnectionError("Could not connect to device") from e

    reply = conn.read()

    if reply != "1;Hello from InoDAQV2":
        LOGGER.error('Handshake returned unknown message: "%s"', reply)
        raise ConnectionError("Handshake returned unknown message")


def toggle_digital_pins(pin: str, state: bool) -> dict[str, bool]:
    pin_id = pin.split("-")[1]

    command = f"dig:{pin_id}:"

    if state:
        command += "on"
    else:
        command += "off"

    LOGGER.info('Sending command: "%s"', command)
    try:
        conn.write(command)
    except errors.InoIOTransmissionError:
        LOGGER.exception("Failed to send command")
        return {"rv": False}

    LOGGER.info('Received reply: "%s"', conn.read())
    return {"rv": True}


def read_analog_pins() -> TYPE_PAYLOAD_AREAD:
    LOGGER.info('Sending command: "aread"')

    try:
        conn.write("aread")
    except errors.InoIOTransmissionError:
        LOGGER.exception("Failed to send command")
        return {
            "rv": False,
            "A0": -1.00,
            "A1": -1.00,
            "A2": -1.00,
            "A3": -1.00,
            "A4": -1.00,
            "A5": -1.00,
        }

    payload = conn.read()
    LOGGER.info('Received reply: "%s"', payload)

    _, values = payload.split(";")
    volts = values.split(",")

    return {
        "rv": True,
        "A0": round(int(volts[0]) * ANALOG_TO_VOLT, 3),
        "A1": round(int(volts[1]) * ANALOG_TO_VOLT, 3),
        "A2": round(int(volts[2]) * ANALOG_TO_VOLT, 3),
        "A3": round(int(volts[3]) * ANALOG_TO_VOLT, 3),
        "A4": round(int(volts[4]) * ANALOG_TO_VOLT, 3),
        "A5": round(int(volts[5]) * ANALOG_TO_VOLT, 3),
    }


def read_digital_pins() -> TYPE_PAYLOAD_DREAD:
    LOGGER.info('Sending command: "dread"')

    try:
        conn.write("dread")
    except errors.InoIOTransmissionError:
        LOGGER.exception("Failed to send command")
        return {
            "rv": False,
            "A0": -1,
            "A1": -1,
            "A2": -1,
            "A3": -1,
            "A4": -1,
            "A5": -1,
        }

    payload = conn.read()
    LOGGER.info('Received reply: "%s"', payload)

    _, values = payload.split(";")
    volts = values.split(",")

    return {
        "rv": True,
        "A0": int(volts[0]),
        "A1": int(volts[1]),
        "A2": int(volts[2]),
        "A3": int(volts[3]),
        "A4": int(volts[4]),
        "A5": int(volts[5]),
    }


def set_pwm(pin: str, value: str) -> dict[str, bool]:
    pin_id = pin.split("-")[1]

    pwm = ceil(int(value) * DUTY_CYCLE_TO_ANALOG)
    command = f"pwm:{pin_id}:{pwm}"

    LOGGER.info('Sending command: "%s"', command)

    try:
        conn.write(command)
    except errors.InoIOTransmissionError:
        LOGGER.exception("Failed to send command")
        return {"rv": False}

    LOGGER.info('Received reply: "%s"', conn.read())
    return {"rv": True}
