import re
from logging import getLogger
from math import ceil, floor
from typing import TypedDict, Union
from inoio import errors
from gui.extensions import conn

LOGGER = getLogger("inodaqv2")
ANALOG_TO_VOLT = 5.0 / 1023
DUTY_CYCLE_TO_ANALOG = 255 / 100
ANALOG_TO_DUTY_CYCLE = 100 / 255
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
PAT_VALID_PWM = re.compile(r"^1;\d{1,2},\d{1,3}$")
PAT_VALID_AREAD = re.compile(r"^1;\d{1,4},\d{1,4},\d{1,4},\d{1,4},\d{1,4},\d{1,4}$")
PAT_VALID_DREAD = re.compile(r"^1;\d{1},\d{1},\d{1},\d{1},\d{1},\d{1}$")
PAT_VALID_TONE = re.compile(r"^1;\d{1},\d{1,5}$")


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


def set_pwm(pin: int, duty_cycle: int) -> TYPE_PAYLOAD_PWM:
    pwm = ceil(duty_cycle * DUTY_CYCLE_TO_ANALOG)
    command = f"pwm:{pin}:{pwm}"

    LOGGER.info('Sending command: "%s"', command)

    try:
        conn.write(command)
    except errors.InoIOTransmissionError:
        LOGGER.exception("Failed to send command")
        return {"rv": False, "pin": pin, "pwm": ""}

    reply = conn.read()
    LOGGER.info('Received reply: "%s"', reply)

    if re.match(PAT_VALID_PWM, reply) is None:
        LOGGER.exception("Could not parse message. Reply is likely garbled")
        return {"rv": False, "pin": pin, "pwm": ""}

    _, values = reply.split(";")
    _pin, _duty_cycle = values.split(",")

    return {
        "rv": True,
        "pin": _pin,
        "pwm": str(floor(int(_duty_cycle) * ANALOG_TO_DUTY_CYCLE)),
    }


def read_analog_pins() -> Union[TYPE_PAYLOAD_AREAD, dict[str, bool]]:
    LOGGER.info('Sending command: "aread"')

    try:
        conn.write("aread")
    except errors.InoIOTransmissionError:
        LOGGER.exception("Failed to send command")
        return {"rv": False}

    reply = conn.read()
    LOGGER.info('Received reply: "%s"', reply)

    if re.match(PAT_VALID_AREAD, reply) is None:
        LOGGER.exception("Could not parse message. Reply is likely garbled")
        return {"rv": False}

    _, values = reply.split(";")
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


def read_digital_pins() -> Union[TYPE_PAYLOAD_DREAD, dict[str, bool]]:
    LOGGER.info('Sending command: "dread"')

    try:
        conn.write("dread")
    except errors.InoIOTransmissionError:
        LOGGER.exception("Failed to send command")
        return {"rv": False}

    reply = conn.read()
    LOGGER.info('Received reply: "%s"', reply)

    if re.match(PAT_VALID_DREAD, reply) is None:
        LOGGER.exception("Could not parse message. Reply is likely garbled")
        return {"rv": False}

    _, values = reply.split(";")
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


def set_tone(pin: int, frequency: str) -> dict[str, bool]:
    if not frequency.isnumeric():
        LOGGER.exception("Cannot convert '%s' to a frequency", frequency)
        return {"rv": False}

    command = f"tone:{pin}:{frequency}"
    LOGGER.info('Sending command: "%s"', command)

    try:
        conn.write(command)
    except errors.InoIOTransmissionError:
        LOGGER.exception("Failed to send command")
        return {"rv": False}

    reply = conn.read()
    LOGGER.info('Received reply: "%s"', reply)

    if re.match(PAT_VALID_TONE, reply) is None:
        LOGGER.exception("Could not parse message. Reply is likely garbled")
        return {"rv": False}

    return {"rv": True}
