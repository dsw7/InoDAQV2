from functools import partial
from logging import getLogger
from math import ceil, floor
from tkinter import Tk, LabelFrame, Scale, Event, IntVar, GROOVE, HORIZONTAL
from inodaqv2.serial_connection import SerialConnection


class PanelPWM:
    logger = getLogger("inodaqv2")

    duty_cycle_to_analog = 255 / 100
    inv_duty_cycle_to_analog = 100 / 255

    def __init__(self, root: Tk, connection: SerialConnection) -> None:
        self.root = root
        self.connection = connection
        self.pins: dict[int, IntVar] = {}
        self.setup_panel()

    def setup_panel(self) -> None:
        frame = LabelFrame(self.root, relief=GROOVE, bd=1, text="PWM")
        frame.pack(
            side="left", fill="both", expand=True, padx=5, pady=5, ipady=3, ipadx=3
        )

        for row, p in enumerate((3, 5, 6, 9, 10, 11)):
            self.pins[p] = IntVar()

            subframe = LabelFrame(frame, relief=GROOVE, bd=1, text=f"Pin {p}")
            subframe.grid(column=1, padx=3, row=row)

            scale = Scale(
                subframe, variable=self.pins[p], orient=HORIZONTAL, length=150
            )
            scale.bind("<ButtonRelease-1>", partial(self.toggle, p))
            scale.grid(column=1, padx=3, row=row)

    def toggle(self, pin: int, *event: Event) -> None:
        pwm = ceil(self.duty_cycle_to_analog * self.pins[pin].get())
        self.logger.debug("Scaled %i up to %i (8 bit range)", self.pins[pin].get(), pwm)

        command = f"pwm:{pin}:{pwm}"

        self.connection.send_message(command)
        status, message = self.connection.receive_message()

        if not status:
            self.logger.error(message)
            return

        pwm = floor(self.inv_duty_cycle_to_analog * int(message.split()[-1]))
        self.logger.info("Pin 11 emitting PWM wave with duty cycle of %i%%", pwm)
