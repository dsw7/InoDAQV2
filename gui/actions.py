import re
from logging import getLogger
from inoio import errors
from gui.extensions import conn

LOGGER = getLogger("inodaqv2")
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
