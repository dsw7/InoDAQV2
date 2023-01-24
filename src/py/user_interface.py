from typing import TypeVar
from math import ceil
from functools import partial
import tkinter as tk
from serial_connection import SerialConnection

T = TypeVar('T')
PACK_FRAME = {'side': 'left', 'fill': 'both', 'expand': True, 'padx': 5, 'pady': 5, 'ipady': 3, 'ipadx': 3}
DUTY_CYCLE_TO_ANALOG = 255 / 100


class PanelDig:

    kw_grid = {'column': 1, 'sticky': 'W', 'padx': 3}

    def __init__(self: T, root: tk.Tk, connection: SerialConnection) -> T:

        self.connection = connection
        self.pins = {}

        frame = tk.LabelFrame(root, relief=tk.GROOVE, bd=1, text='Digital')
        frame.pack(**PACK_FRAME)

        for p in range(2, 14):
            self.pins[p] = tk.BooleanVar()
            tk.Checkbutton(frame, text=f'Pin {p}', variable=self.pins[p], command=partial(self.toggle, p)).grid(**self.kw_grid, row=p)

    def toggle(self: T, pin: int) -> None:
        command = f'dig:{pin}:'

        if self.pins[pin].get():
            command += 'on'
        else:
            command += 'off'

        self.connection.send_message(command)
        self.connection.receive_message()


class PanelPWM:

    kw_button = {'column': 1, 'padx': 3}
    kw_scale = {'column': 2, 'padx': 3}

    def __init__(self: T, root: tk.Tk, connection: SerialConnection) -> T:

        self.connection = connection
        self.pins = {}

        frame = tk.LabelFrame(root, relief=tk.GROOVE, bd=1, text='PWM')
        frame.pack(**PACK_FRAME)

        for row, p in enumerate((3, 5, 6, 9, 10, 11), 2):
            self.pins[p] = tk.IntVar()
            tk.Button(frame, text=p, command=partial(self.toggle, p), width=3).grid(**self.kw_button, row=row)
            tk.Scale(frame, variable=self.pins[p], orient=tk.HORIZONTAL).grid(**self.kw_scale, row=row)

    def toggle(self: T, pin: int) -> None:
        pwm = ceil(DUTY_CYCLE_TO_ANALOG * self.pins[pin].get())
        command = f'pwm:{pin}:{pwm}'

        self.connection.send_message(command)
        self.connection.receive_message()
