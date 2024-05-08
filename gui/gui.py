import sys
from tkinter import Tk, _tkinter
from tkinter import ttk

try:
    root = Tk()
except _tkinter.TclError as exception:
    sys.exit(f'Missing X11 graphic layer: "{exception}"')


def main() -> None:
    root.title("InoDAQV2")

    frm = ttk.Frame(root, padding=10)
    frm.grid()

    ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)

    root.mainloop()


if __name__ == "__main__":
    main()
