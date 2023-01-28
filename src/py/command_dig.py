from functools import partial
from tkinter import LabelFrame, Checkbutton
from tkinter import GROOVE, BooleanVar
from base import PanelBase, T


class PanelDig(PanelBase):

    kw_button = {'column': 1, 'sticky': 'W', 'padx': 3}

    def setup_panel(self: T) -> None:

        frame = LabelFrame(self.root, relief=GROOVE, bd=1, text='Digital')
        frame.pack(**self.kw_labelframe)

        for p in range(2, 14):
            self.pins[p] = BooleanVar()
            Checkbutton(frame, text=f'Pin {p}', variable=self.pins[p], command=partial(self.toggle, p)).grid(**self.kw_button, row=p - 2)

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
