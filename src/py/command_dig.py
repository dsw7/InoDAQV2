from logging import getLogger
from functools import partial
from tkinter import Tk, LabelFrame, Checkbutton, GROOVE, BooleanVar
from serial_connection import SerialConnection


class PanelDig:
    logger = getLogger("inodaqv2")

    def __init__(self, root: Tk, connection: SerialConnection) -> None:
        self.root = root
        self.connection = connection
        self.pins: dict[int, BooleanVar] = {}
        self.setup_panel()

    def setup_panel(self) -> None:
        frame = LabelFrame(self.root, relief=GROOVE, bd=1, text="Digital")
        frame.pack(
            side="left", fill="both", expand=True, padx=5, pady=5, ipady=3, ipadx=3
        )

        for p in range(2, 14):
            self.pins[p] = BooleanVar()
            Checkbutton(
                frame,
                text=f"Pin {p}",
                variable=self.pins[p],
                command=partial(self.toggle, p),
            ).grid(column=1, sticky="W", padx=3, row=p - 2)

    def toggle(self, pin: int) -> None:
        command = f"dig:{pin}:"

        if self.pins[pin].get():
            command += "on"
        else:
            command += "off"

        self.connection.send_message(command)
        status, message = self.connection.receive_message()

        if status:
            self.logger.info(message)
        else:
            self.logger.error(message)
