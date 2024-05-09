from functools import partial
from re import match
from tkinter import Tk, ttk, BooleanVar
from inoio import errors
from gui.consts import LOGGER, PAT_VALID_DIG, PADDING_FRAME, MARGIN_Y, MARGIN_X
from gui.extensions import conn

_PINS_DIGITAL: dict[int, BooleanVar] = {p: BooleanVar() for p in range(2, 14)}


def toggle_digital_pins(pin: int) -> None:
    command = f"dig:{pin}:"

    if _PINS_DIGITAL[pin].get():
        command += "on"
    else:
        command += "off"

    LOGGER.info('Sending command: "%s"', command)
    try:
        conn.write(command)
    except errors.InoIOTransmissionError:
        LOGGER.exception("Failed to send command")
        return

    reply = conn.read()
    LOGGER.info('Received reply: "%s"', reply)

    if match(PAT_VALID_DIG, reply) is None:
        LOGGER.exception("Could not parse message. Reply is likely garbled")
        return


def frame_digital_pins(root: Tk) -> None:
    frame = ttk.LabelFrame(root, padding=PADDING_FRAME, text="Digital")
    frame.grid(
        row=0, column=0, sticky="ns", padx=(MARGIN_X * 2, MARGIN_X), pady=MARGIN_Y
    )

    for pin, state in _PINS_DIGITAL.items():
        ttk.Checkbutton(
            frame,
            text=f"Pin {pin}",
            variable=state,
            command=partial(toggle_digital_pins, pin),
        ).grid(sticky="w", pady=(5, 0), row=pin - 2)
