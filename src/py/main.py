import typing
import tkinter as tk

T = typing.TypeVar('T')


class PanelDig:

    def __init__(self: T, master: tk.Tk) -> T:

        frame = tk.LabelFrame(master, relief=tk.GROOVE, bd=1, text='Toggle digital pins')
        frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        self.pins = {}

        for p in range(2, 14):
            pin = f'Pin {p}'
            self.pins[pin] = tk.BooleanVar()

            tk.Checkbutton(
                frame, text=pin, variable=self.pins[pin], command=self.toggle
            ).grid(column=1, sticky='W', row=p, padx=5)

    def toggle(self: T) -> None:
        print(self.pins)


class PanelPWM:

    def __init__(self: T, master: tk.Tk) -> T:

        frame = tk.LabelFrame(master, relief=tk.GROOVE, bd=1, text='Replace')
        frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)

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
