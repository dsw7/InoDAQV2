from logging import getLogger
from abc import ABC, abstractmethod
from typing import TypeVar
from math import ceil, floor
from functools import partial
import tkinter as tk
from serial_connection import SerialConnection

T = TypeVar('T')


class PanelBase(ABC):

    logger = getLogger('inodaqv2')

    kw_labelframe = {
        'side': 'left', 'fill': 'both', 'expand': True, 'padx': 5, 'pady': 5, 'ipady': 3, 'ipadx': 3
    }

    def __init__(self: T, root: tk.Tk, connection: SerialConnection) -> T:

        self.root = root
        self.connection = connection
        self.pins = {}
        self.setup_panel()

    @abstractmethod
    def setup_panel(self: T) -> None:
        pass

    @abstractmethod
    def toggle(self: T, pin: int) -> None:
        pass


class PanelDig(PanelBase):

    kw_button = {'column': 1, 'sticky': 'W', 'padx': 3}

    def setup_panel(self: T) -> None:

        frame = tk.LabelFrame(self.root, relief=tk.GROOVE, bd=1, text='Digital')
        frame.pack(**self.kw_labelframe)

        for p in range(2, 14):
            self.pins[p] = tk.BooleanVar()
            tk.Checkbutton(frame, text=f'Pin {p}', variable=self.pins[p], command=partial(self.toggle, p)).grid(**self.kw_button, row=p)

    def toggle(self: T, pin: int) -> None:

        command = f'dig:{pin}:'

        if self.pins[pin].get():
            command += 'on'
        else:
            command += 'off'

        self.connection.send_message(command)
        status, message = self.connection.receive_message()

        if status:
            self.logger.info(message)
        else:
            self.logger.error(message)


class PanelPWM(PanelBase):

    kw_button = {'column': 1, 'padx': 3}
    kw_scale = {'column': 2, 'padx': 3}

    duty_cycle_to_analog = 255 / 100
    inv_duty_cycle_to_analog = 100 / 255

    def setup_panel(self: T) -> None:

        frame = tk.LabelFrame(self.root, relief=tk.GROOVE, bd=1, text='PWM')
        frame.pack(**self.kw_labelframe)

        for row, p in enumerate((3, 5, 6, 9, 10, 11), 2):
            self.pins[p] = tk.IntVar()
            tk.Button(frame, text=p, command=partial(self.toggle, p), width=3).grid(**self.kw_button, row=row)
            tk.Scale(frame, variable=self.pins[p], orient=tk.HORIZONTAL).grid(**self.kw_scale, row=row)

    def toggle(self: T, pin: int) -> None:

        pwm = ceil(self.duty_cycle_to_analog * self.pins[pin].get())
        self.logger.debug('Scaled %i up to %i (8 bit range)', self.pins[pin].get(), pwm)

        command = f'pwm:{pin}:{pwm}'

        self.connection.send_message(command)
        status, message = self.connection.receive_message()

        if not status:
            self.logger.error(message)
            return

        pwm = floor(self.inv_duty_cycle_to_analog * int(message.split()[-1]))
        self.logger.info('Pin 11 emitting PWM wave with duty cycle of %i%%', pwm)
