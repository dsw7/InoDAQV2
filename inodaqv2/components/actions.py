from logging import getLogger
from math import ceil, floor
from re import compile
from typing import TypedDict
from inoio import errors
from inodaqv2.components.extensions import conn

LOGGER = getLogger("inodaqv2")
ANALOG_TO_VOLT = 5.0 / 1023
DUTY_CYCLE_TO_ANALOG = 255 / 100
ANALOG_TO_DUTY_CYCLE = 100 / 255

TYPE_PAYLOAD_DIG = TypedDict(
    "TYPE_PAYLOAD_DIG",
    {
        "rv": bool,
        "pin": str,
        "state": str,
    },
)
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
TYPE_PAYLOAD_PWM = TypedDict(
    "TYPE_PAYLOAD_PWM",
    {
        "rv": bool,
        "pin": str,
        "pwm": str,
    },
)

PAYLOAD_AREAD_ERR: TYPE_PAYLOAD_AREAD = {
    "rv": False,
    "A0": -1.00,
    "A1": -1.00,
    "A2": -1.00,
    "A3": -1.00,
    "A4": -1.00,
    "A5": -1.00,
}
PAYLOAD_DREAD_ERR: TYPE_PAYLOAD_DREAD = {
    "rv": False,
    "A0": -1,
    "A1": -1,
    "A2": -1,
    "A3": -1,
    "A4": -1,
    "A5": -1,
}

PAT_VALID_DIG = compile("^1;\d{1,2},(on|off)$")


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


def toggle_digital_pins(pin: str, state: bool) -> TYPE_PAYLOAD_DIG:
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
        return {"rv": False, "pin": pin_id, "state": "ERR"}

    payload = conn.read()
    LOGGER.info('Received reply: "%s"', payload)

    try:
        _, values = payload.split(";")
    except ValueError:
        LOGGER.exception("Could not parse message. Reply is likely garbled")
        return {"rv": False, "pin": pin_id, "state": "ERR"}

    _pin, _state = values.split(",")

    return {"rv": True, "pin": _pin, "state": _state}


def read_analog_pins() -> TYPE_PAYLOAD_AREAD:
    LOGGER.info('Sending command: "aread"')

    try:
        conn.write("aread")
    except errors.InoIOTransmissionError:
        LOGGER.exception("Failed to send command")
        return PAYLOAD_AREAD_ERR

    payload = conn.read()
    LOGGER.info('Received reply: "%s"', payload)

    try:
        _, values = payload.split(";")
    except ValueError:
        LOGGER.exception("Could not parse message. Reply is likely garbled")
        return PAYLOAD_AREAD_ERR

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
        return PAYLOAD_DREAD_ERR

    payload = conn.read()
    LOGGER.info('Received reply: "%s"', payload)

    try:
        _, values = payload.split(";")
    except ValueError:
        LOGGER.exception("Could not parse message. Reply is likely garbled")
        return PAYLOAD_DREAD_ERR

    state = values.split(",")

    return {
        "rv": True,
        "A0": int(state[0]),
        "A1": int(state[1]),
        "A2": int(state[2]),
        "A3": int(state[3]),
        "A4": int(state[4]),
        "A5": int(state[5]),
    }


def set_pwm(pin: str, duty_cycle: str) -> TYPE_PAYLOAD_PWM:
    pin_id = pin.split("-")[1]

    pwm = ceil(int(duty_cycle) * DUTY_CYCLE_TO_ANALOG)
    command = f"pwm:{pin_id}:{pwm}"

    LOGGER.info('Sending command: "%s"', command)

    try:
        conn.write(command)
    except errors.InoIOTransmissionError:
        LOGGER.exception("Failed to send command")
        return {"rv": False, "pin": pin_id, "pwm": "ERR"}

    payload = conn.read()
    LOGGER.info('Received reply: "%s"', payload)

    try:
        _, values = payload.split(";")
    except ValueError:
        LOGGER.exception("Could not parse message. Reply is likely garbled")
        return {"rv": False, "pin": pin_id, "pwm": "ERR"}

    _pin, _duty_cycle = values.split(",")

    return {
        "rv": True,
        "pin": _pin,
        "pwm": str(floor(int(_duty_cycle) * ANALOG_TO_DUTY_CYCLE)),
    }
