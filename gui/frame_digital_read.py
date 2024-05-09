from re import match
from tkinter import Tk, ttk, Text, Button
from inoio import errors
from gui.consts import LOGGER, PAT_VALID_DREAD, PADDING_FRAME, MARGIN_Y, MARGIN_X
from gui.extensions import conn

_PINS_DREAD: dict[int, Text] = {}


def read_digital_pins() -> None:
    LOGGER.info('Sending command: "dread"')

    try:
        conn.write("dread")
    except errors.InoIOTransmissionError:
        LOGGER.exception("Failed to send command")
        return

    reply = conn.read()
    LOGGER.info('Received reply: "%s"', reply)

    if match(PAT_VALID_DREAD, reply) is None:
        LOGGER.exception("Could not parse message. Reply is likely garbled")
        return

    _, values = reply.split(";")
    states = values.split(",")

    for pin, state in enumerate(states):
        _PINS_DREAD[pin].delete(1.0, "end")
        _PINS_DREAD[pin].insert("end", state)


def frame_digital_read(root: Tk) -> None:
    frame = ttk.LabelFrame(root, padding=PADDING_FRAME, text="Digital Read")
    frame.grid(row=0, column=3, sticky="ns", padx=MARGIN_X, pady=MARGIN_Y)

    for pin in range(0, 6):
        subframe = ttk.LabelFrame(frame, text=f"A{pin}")
        subframe.grid(row=pin, pady=(0, 5))

        _PINS_DREAD[pin] = Text(subframe, height=1, width=12)
        _PINS_DREAD[pin].grid(row=pin)
        _PINS_DREAD[pin].insert("end", "...")

    Button(frame, text="READ", command=read_digital_pins).grid(pady=(5, 10))
