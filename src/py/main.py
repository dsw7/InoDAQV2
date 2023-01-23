import typing
import tkinter as tk

T = typing.TypeVar('T')
PACK_FRAME = {'side': 'left', 'fill': 'both', 'expand': True, 'padx': 5, 'pady': 5}
PACK_GRID = {'column': 1, 'sticky': 'W', 'padx': 5}


class PanelDig:

    def __init__(self: T, master: tk.Tk) -> T:

        frame = tk.LabelFrame(master, relief=tk.GROOVE, bd=1, text='Toggle digital pins')
        frame.pack(**PACK_FRAME)

        self.pins = {}

        for pin in range(2, 14):
            self.pins[pin] = tk.BooleanVar()

        tk.Checkbutton(frame, text='Pin 2', variable=self.pins[2], command=lambda: self.toggle(2)).grid(**PACK_GRID, row=2)
        tk.Checkbutton(frame, text='Pin 3', variable=self.pins[3], command=lambda: self.toggle(3)).grid(**PACK_GRID, row=3)
        tk.Checkbutton(frame, text='Pin 4', variable=self.pins[4], command=lambda: self.toggle(4)).grid(**PACK_GRID, row=4)
        tk.Checkbutton(frame, text='Pin 5', variable=self.pins[5], command=lambda: self.toggle(5)).grid(**PACK_GRID, row=5)
        tk.Checkbutton(frame, text='Pin 6', variable=self.pins[6], command=lambda: self.toggle(6)).grid(**PACK_GRID, row=6)
        tk.Checkbutton(frame, text='Pin 7', variable=self.pins[7], command=lambda: self.toggle(7)).grid(**PACK_GRID, row=7)
        tk.Checkbutton(frame, text='Pin 8', variable=self.pins[8], command=lambda: self.toggle(8)).grid(**PACK_GRID, row=8)
        tk.Checkbutton(frame, text='Pin 9', variable=self.pins[9], command=lambda: self.toggle(9)).grid(**PACK_GRID, row=9)
        tk.Checkbutton(frame, text='Pin 10', variable=self.pins[10], command=lambda: self.toggle(10)).grid(**PACK_GRID, row=10)
        tk.Checkbutton(frame, text='Pin 11', variable=self.pins[11], command=lambda: self.toggle(11)).grid(**PACK_GRID, row=11)
        tk.Checkbutton(frame, text='Pin 12', variable=self.pins[12], command=lambda: self.toggle(12)).grid(**PACK_GRID, row=12)
        tk.Checkbutton(frame, text='Pin 13', variable=self.pins[13], command=lambda: self.toggle(13)).grid(**PACK_GRID, row=13)

    def toggle(self: T, pin: int) -> None:
        print(pin, self.pins[pin].get())


class PanelPWM:

    def __init__(self: T, master: tk.Tk) -> T:

        frame = tk.LabelFrame(master, relief=tk.GROOVE, bd=1, text='Replace')
        frame.pack(**PACK_FRAME)

        tk.Label(frame, text='Enter ID here:').pack(anchor='w', padx=5)
        self._id = tk.Entry(frame)
        self._id.pack(fill='x', padx=5)
        self._id.insert(tk.END, '123')

        tk.Button(frame, text='Replace', command=self.button_replace_callback).pack(
            fill='x', side='bottom', padx=5, pady=5
        )

    def button_replace_callback(self):
        print('Entry ID:', self._id.get())


class Master:
    def __init__(self, master):
        master.title('Unknown')
        master.geometry('1200x300')

        PanelDig(master)
        PanelPWM(master)


def main():
    root = tk.Tk()
    Master(root)
    root.mainloop()

if __name__ == '__main__':
    main()
