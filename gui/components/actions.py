import re
from logging import getLogger
from math import ceil, floor
from typing import TypedDict, Union
from inoio import errors
from gui.components.extensions import conn

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
PAT_VALID_DIG = re.compile(r"^1;\d{1,2},(on|off)$")
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
        return {"rv": False, "pin": pin_id, "state": ""}

    reply = conn.read()
    LOGGER.info('Received reply: "%s"', reply)

    if re.match(PAT_VALID_DIG, reply) is None:
        LOGGER.exception("Could not parse message. Reply is likely garbled")
        return {"rv": False, "pin": pin_id, "state": ""}

    _, values = reply.split(";")
    _pin, _state = values.split(",")

    return {"rv": True, "pin": _pin, "state": _state}


def set_pwm(pin: str, duty_cycle: str) -> TYPE_PAYLOAD_PWM:
    pin_id = pin.split("-")[1]

    pwm = ceil(int(duty_cycle) * DUTY_CYCLE_TO_ANALOG)
    command = f"pwm:{pin_id}:{pwm}"

    LOGGER.info('Sending command: "%s"', command)

    try:
        conn.write(command)
    except errors.InoIOTransmissionError:
        LOGGER.exception("Failed to send command")
        return {"rv": False, "pin": pin_id, "pwm": ""}

    reply = conn.read()
    LOGGER.info('Received reply: "%s"', reply)

    if re.match(PAT_VALID_PWM, reply) is None:
        LOGGER.exception("Could not parse message. Reply is likely garbled")
        return {"rv": False, "pin": pin_id, "pwm": ""}

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


def set_tone(pin: str, frequency: str) -> dict[str, bool]:
    if not frequency.isnumeric():
        LOGGER.exception("Cannot convert '%s' to a frequency", frequency)
        return {"rv": False}

    pin_id = pin.split("-")[1]

    command = f"tone:{pin_id}:{frequency}"
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
