from tkinter import LabelFrame, Text, Button
from tkinter import GROOVE, END
from base import PanelBase, T


class PanelAread(PanelBase):

    kw_label_text = {'column': 1, 'padx': 3, 'pady': 3}
    kw_button = {'column': 1, 'pady': 3, 'row': 6}

    analog_to_volt = 5.0 / 1023

    def setup_panel(self: T) -> None:

        frame = LabelFrame(self.root, relief=GROOVE, bd=1, text='AnalogRead')
        frame.pack(**self.kw_labelframe)

        for p in range(0, 6):
            subframe = LabelFrame(frame, relief=GROOVE, bd=1, text=f'A{p}')
            subframe.grid(**self.kw_label_text, row=p)

            self.pins[p] = Text(subframe, height=1, width=20)
            self.pins[p].grid(**self.kw_label_text, row=p)

            self.pins[p].insert(END, ' ...')

        Button(frame, text='READ', command=self.toggle).grid(**self.kw_button)

    def toggle(self: T) -> None:

        self.connection.send_message('aread')
        status, message = self.connection.receive_message()

        if not status:
            self.logger.error(message)
            return

        volts = [round(int(i) * self.analog_to_volt, 3) for i in message.split(',')]

        for p in range(0, 6):
            self.pins[p].delete(1.0, END)
            self.pins[p].insert(END, volts[p])
