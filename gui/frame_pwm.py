from functools import partial
from math import ceil, floor
from re import match
from tkinter import Tk, ttk, IntVar
from inoio import errors
from gui.consts import LOGGER, PAT_VALID_PWM, PADDING_FRAME, MARGIN_Y, MARGIN_X
from gui.extensions import conn

_ANALOG_TO_DUTY_CYCLE = 100 / 255
_DUTY_CYCLE_TO_ANALOG = 255 / 100
_PINS_PWM: dict[int, IntVar] = {}


def set_pwm(pin: int, *event) -> None:
    pwm = ceil(_PINS_PWM[pin].get() * _DUTY_CYCLE_TO_ANALOG)
    LOGGER.info("Scaled %i up to %i (8 bit range)", _PINS_PWM[pin].get(), pwm)

    command = f"pwm:{pin}:{pwm}"
    LOGGER.info('Sending command: "%s"', command)

    try:
        conn.write(command)
    except errors.InoIOTransmissionError:
        LOGGER.exception("Failed to send command")
        return

    reply = conn.read()
    LOGGER.info('Received reply: "%s"', reply)

    if match(PAT_VALID_PWM, reply) is None:
        LOGGER.exception("Could not parse message. Reply is likely garbled")
        return

    _, values = reply.split(";")
    _pin, _pwm = values.split(",")

    duty_cycle = floor(int(_pwm) * _ANALOG_TO_DUTY_CYCLE)
    LOGGER.info("Pin %s emitting PWM wave with duty cycle of %i%%", _pin, duty_cycle)


def frame_pwm(root: Tk) -> None:
    frame = ttk.LabelFrame(root, padding=PADDING_FRAME, text="PWM")
    frame.grid(row=0, column=1, sticky="ns", padx=MARGIN_X, pady=MARGIN_Y)

    for row, p in enumerate((3, 5, 6, 9, 10, 11)):
        _PINS_PWM[p] = IntVar()

        subframe = ttk.LabelFrame(frame, text=f"Pin {p}")
        subframe.grid(pady=(5, 0), row=row)

        scale = ttk.Scale(subframe, variable=_PINS_PWM[p], from_=0, to=100, length=150)
        scale.bind("<ButtonRelease-1>", partial(set_pwm, p))
        scale.grid(row=row)
