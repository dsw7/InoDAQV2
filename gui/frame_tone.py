from re import match
from tkinter import Tk, ttk, IntVar, _tkinter, messagebox
from inoio import errors
from gui.consts import LOGGER, PAT_VALID_TONE, PADDING_FRAME, MARGIN_Y, MARGIN_X
from gui.extensions import conn

_PIN = IntVar()
_FREQUENCY = IntVar()


def set_tone() -> None:
    try:
        frequency = _FREQUENCY.get()
    except _tkinter.TclError:
        messagebox.showerror("Error", "Invalid frequency was provided")
        LOGGER.exception("Invalid frequency was provided")
        return

    if (frequency < 31) or (frequency > 65535):
        messagebox.showerror("Error", "Frequency must be between 31 and 65535 Hz")
        LOGGER.exception("Frequency must be between 31 and 65535 Hz")
        return

    command = f"tone:{_PIN.get()}:{frequency}"
    LOGGER.info('Sending command: "%s"', command)

    try:
        conn.write(command)
    except errors.InoIOTransmissionError as e:
        LOGGER.exception("Failed to send command")
        messagebox.showerror("Error", e)
        return

    reply = conn.read()
    LOGGER.info('Received reply: "%s"', reply)

    if match(PAT_VALID_TONE, reply) is None:
        LOGGER.error("Could not parse message. Reply is likely garbled")
        messagebox.showerror("Error", "Could not parse message")


def frame_tone(root: Tk) -> None:
    frame = ttk.LabelFrame(root, padding=PADDING_FRAME, text="Tone")
    frame.grid(
        row=0, column=4, sticky="ns", padx=(MARGIN_X, MARGIN_X * 2), pady=MARGIN_Y
    )

    ttk.Radiobutton(frame, text="Pin 2", variable=_PIN, value=2, command=set_tone).grid(
        sticky="w", pady=(0, 5)
    )
    ttk.Radiobutton(frame, text="Pin 4", variable=_PIN, value=4, command=set_tone).grid(
        sticky="w", pady=(0, 5)
    )
    ttk.Radiobutton(frame, text="Pin 7", variable=_PIN, value=7, command=set_tone).grid(
        sticky="w", pady=(0, 5)
    )
    ttk.Radiobutton(frame, text="Pin 8", variable=_PIN, value=8, command=set_tone).grid(
        sticky="w", pady=(0, 5)
    )

    subframe = ttk.LabelFrame(frame, padding=PADDING_FRAME, text="Frequency (Hz)")
    subframe.grid(pady=(5, 0))
    ttk.Entry(subframe, textvariable=_FREQUENCY).pack()
