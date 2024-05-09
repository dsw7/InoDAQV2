from re import match
from tkinter import Tk, ttk, IntVar, _tkinter
from inoio import errors
from gui.consts import LOGGER, PAT_VALID_TONE
from gui.extensions import conn

_PIN = IntVar()
_FREQUENCY = IntVar()


def set_tone() -> None:
    try:
        frequency = _FREQUENCY.get()
    except _tkinter.TclError:
        LOGGER.exception("Invalid frequency was provided")
        return

    command = f"tone:{_PIN.get()}:{frequency}"
    LOGGER.info('Sending command: "%s"', command)

    try:
        conn.write(command)
    except errors.InoIOTransmissionError:
        LOGGER.exception("Failed to send command")
        return

    reply = conn.read()
    LOGGER.info('Received reply: "%s"', reply)

    if match(PAT_VALID_TONE, reply) is None:
        LOGGER.exception("Could not parse message. Reply is likely garbled")
        return


def frame_tone(root: Tk) -> None:
    frame = ttk.LabelFrame(root, padding=10, text="Tone")
    frame.grid(row=0, column=4, sticky="ns", padx=(10, 20), pady=20)

    ttk.Radiobutton(frame, text="Pin 2", variable=_PIN, value=2, command=set_tone).grid(
        sticky="w"
    )
    ttk.Radiobutton(frame, text="Pin 4", variable=_PIN, value=4, command=set_tone).grid(
        sticky="w"
    )
    ttk.Radiobutton(frame, text="Pin 7", variable=_PIN, value=7, command=set_tone).grid(
        sticky="w"
    )
    ttk.Radiobutton(frame, text="Pin 8", variable=_PIN, value=8, command=set_tone).grid(
        sticky="w"
    )

    subframe = ttk.LabelFrame(frame, padding=10, text="Frequency (Hz)")
    subframe.grid()
    ttk.Entry(subframe, textvariable=_FREQUENCY).pack()
