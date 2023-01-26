from math import ceil, floor
from functools import partial
from tkinter import LabelFrame, Button, Scale
from tkinter import IntVar, GROOVE, HORIZONTAL
from base import PanelBase, T


class PanelPWM(PanelBase):

    kw_button = {'column': 1, 'padx': 3}
    kw_scale = {'column': 2, 'padx': 3}

    duty_cycle_to_analog = 255 / 100
    inv_duty_cycle_to_analog = 100 / 255

    def setup_panel(self: T) -> None:

        frame = LabelFrame(self.root, relief=GROOVE, bd=1, text='PWM')
        frame.pack(**self.kw_labelframe)

        for row, p in enumerate((3, 5, 6, 9, 10, 11), 2):
            self.pins[p] = IntVar()
            Button(frame, text=p, command=partial(self.toggle, p), width=3).grid(**self.kw_button, row=row)
            Scale(frame, variable=self.pins[p], orient=HORIZONTAL, length=150).grid(**self.kw_scale, row=row)

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
