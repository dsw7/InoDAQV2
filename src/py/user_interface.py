import tkinter as tk
from serial_connection import SerialConnection
import consts


class PanelDig:

    def __init__(self: consts.T, root: tk.Tk, connection: SerialConnection) -> consts.T:

        self.connection = connection
        self.pins = {}

        frame = tk.LabelFrame(root, relief=tk.GROOVE, bd=1, text='Toggle digital pins')
        frame.pack(**consts.PACK_FRAME)

        for pin in range(2, 14):
            self.pins[pin] = tk.BooleanVar()

        tk.Checkbutton(frame, text='Pin 2', variable=self.pins[2], command=lambda: self.toggle(2)).grid(**consts.PACK_GRID, row=2)
        tk.Checkbutton(frame, text='Pin 3', variable=self.pins[3], command=lambda: self.toggle(3)).grid(**consts.PACK_GRID, row=3)
        tk.Checkbutton(frame, text='Pin 4', variable=self.pins[4], command=lambda: self.toggle(4)).grid(**consts.PACK_GRID, row=4)
        tk.Checkbutton(frame, text='Pin 5', variable=self.pins[5], command=lambda: self.toggle(5)).grid(**consts.PACK_GRID, row=5)
        tk.Checkbutton(frame, text='Pin 6', variable=self.pins[6], command=lambda: self.toggle(6)).grid(**consts.PACK_GRID, row=6)
        tk.Checkbutton(frame, text='Pin 7', variable=self.pins[7], command=lambda: self.toggle(7)).grid(**consts.PACK_GRID, row=7)
        tk.Checkbutton(frame, text='Pin 8', variable=self.pins[8], command=lambda: self.toggle(8)).grid(**consts.PACK_GRID, row=8)
        tk.Checkbutton(frame, text='Pin 9', variable=self.pins[9], command=lambda: self.toggle(9)).grid(**consts.PACK_GRID, row=9)
        tk.Checkbutton(frame, text='Pin 10', variable=self.pins[10], command=lambda: self.toggle(10)).grid(**consts.PACK_GRID, row=10)
        tk.Checkbutton(frame, text='Pin 11', variable=self.pins[11], command=lambda: self.toggle(11)).grid(**consts.PACK_GRID, row=11)
        tk.Checkbutton(frame, text='Pin 12', variable=self.pins[12], command=lambda: self.toggle(12)).grid(**consts.PACK_GRID, row=12)
        tk.Checkbutton(frame, text='Pin 13', variable=self.pins[13], command=lambda: self.toggle(13)).grid(**consts.PACK_GRID, row=13)

    def toggle(self: consts.T, pin: int) -> None:
        command = f'dig:{pin}:'

        if self.pins[pin].get():
            command += 'on'
        else:
            command += 'off'

        self.connection.send_message(command)
        self.connection.receive_message()


class PanelPWM:

    def __init__(self: consts.T, root: tk.Tk) -> consts.T:

        frame = tk.LabelFrame(root, relief=tk.GROOVE, bd=1, text='Replace')
        frame.pack(**consts.PACK_FRAME)

        tk.Label(frame, text='Enter ID here:').pack(anchor='w', padx=5)
        self._id = tk.Entry(frame)
        self._id.pack(fill='x', padx=5)
        self._id.insert(tk.END, '123')

        tk.Button(frame, text='Replace', command=self.button_replace_callback).pack(
            fill='x', side='bottom', padx=5, pady=5
        )

    def button_replace_callback(self):
        print('Entry ID:', self._id.get())
