from logging import getLogger
from tkinter import Tk, LabelFrame, Text, Button, GROOVE, END
from serial_connection import SerialConnection


class PanelDread:
    logger = getLogger("inodaqv2")

    def __init__(self, root: Tk, connection: SerialConnection) -> None:
        self.root = root
        self.connection = connection
        self.pins: dict[int, Text] = {}
        self.setup_panel()

    def setup_panel(self) -> None:
        frame = LabelFrame(self.root, relief=GROOVE, bd=1, text="DigitalRead")
        frame.pack(
            side="left", fill="both", expand=True, padx=5, pady=5, ipady=3, ipadx=3
        )

        for p in range(0, 6):
            subframe = LabelFrame(frame, relief=GROOVE, bd=1, text=f"A{p}")
            subframe.grid(column=1, padx=3, pady=3, row=p)

            self.pins[p] = Text(subframe, height=1, width=20)
            self.pins[p].grid(column=1, padx=3, pady=3, row=p)

            self.pins[p].insert(END, " ...")

        Button(frame, text="READ", command=self.toggle).grid(column=1, pady=3, row=6)

    def toggle(self) -> None:
        self.connection.send_message("dread")
        status, message = self.connection.receive_message()

        if not status:
            self.logger.error(message)
            return

        for p, state in enumerate(message.split(",")):
            self.pins[p].delete(1.0, END)
            self.pins[p].insert(END, state)
