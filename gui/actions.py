import re
from logging import getLogger
from typing import TypedDict, Union
from inoio import errors
from gui.extensions import conn

LOGGER = getLogger("inodaqv2")
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
