from re import match
from tkinter import Tk, ttk, Text, Button
from inoio import errors
from gui.consts import LOGGER, PAT_VALID_AREAD, PADDING_FRAME, MARGIN_Y, MARGIN_X
from gui.extensions import conn

_ANALOG_TO_VOLT = 5.0 / 1023
_PINS_AREAD: dict[int, Text] = {}


def read_analog_pins() -> None:
    LOGGER.info('Sending command: "aread"')

    try:
        conn.write("aread")
    except errors.InoIOTransmissionError:
        LOGGER.exception("Failed to send command")
        return

    reply = conn.read()
    LOGGER.info('Received reply: "%s"', reply)

    if match(PAT_VALID_AREAD, reply) is None:
        LOGGER.exception("Could not parse message. Reply is likely garbled")
        return

    _, values = reply.split(";")
    volts = values.split(",")

    for pin in range(0, 6):
        _PINS_AREAD[pin].delete(1.0, "end")
        _PINS_AREAD[pin].insert("end", str(round(int(volts[pin]) * _ANALOG_TO_VOLT, 3)))


def frame_analog_read(root: Tk) -> None:
    frame = ttk.LabelFrame(root, padding=PADDING_FRAME, text="Analog Read")
    frame.grid(row=0, column=2, sticky="ns", padx=MARGIN_X, pady=MARGIN_Y)

    for pin in range(0, 6):
        subframe = ttk.LabelFrame(frame, text=f"A{pin}")
        subframe.grid(row=pin)

        _PINS_AREAD[pin] = Text(subframe, height=1, width=20)
        _PINS_AREAD[pin].grid(row=pin)
        _PINS_AREAD[pin].insert("end", "...")

    Button(frame, text="READ", command=read_analog_pins).grid(pady=(20, 0))
