import sys
from functools import partial
from tkinter import BooleanVar
from tkinter import Tk, ttk, _tkinter

try:
    root = Tk()
except _tkinter.TclError as exception:
    sys.exit(f'Missing X11 graphic layer: "{exception}"')

PINS_DIGITAL: dict[int, BooleanVar] = {p: BooleanVar() for p in range(2, 14)}


def toggle_pin(pin):
    print(PINS_DIGITAL[pin].get())


def panel_dig() -> None:
    frame = ttk.LabelFrame(root, padding=10, text="Digital")
    frame.grid(row=0, column=0, sticky="ns", padx=2)

    for pin, state in PINS_DIGITAL.items():
        ttk.Checkbutton(
            frame, text=f"Pin {pin}", variable=state, command=partial(toggle_pin, pin)
        ).grid(sticky="w", column=0, row=pin - 2)


def panel_pwm() -> None:
    frame = ttk.LabelFrame(root, padding=10, text="PWM")
    frame.grid(row=0, column=1, sticky="ns", padx=2)

    ttk.Button(frame, text="Quit", command=root.destroy).grid(column=1, row=0)


def panel_analog_read() -> None:
    frame = ttk.LabelFrame(root, padding=10, text="Analog Read")
    frame.grid(row=0, column=2, sticky="ns", padx=2)

    ttk.Button(frame, text="Quit", command=root.destroy).grid(column=1, row=0)


def panel_digital_read() -> None:
    frame = ttk.LabelFrame(root, padding=10, text="Digital Read")
    frame.grid(row=0, column=3, sticky="ns", padx=2)

    ttk.Button(frame, text="Quit", command=root.destroy).grid(column=1, row=0)
    ttk.Button(frame, text="Quit", command=root.destroy).grid(column=1, row=1)


def panel_tone() -> None:
    frame = ttk.LabelFrame(root, padding=10, text="Tone")
    frame.grid(row=0, column=4, sticky="ns", padx=2)

    ttk.Button(frame, text="Quit", command=root.destroy).grid(column=1, row=0)


def main() -> None:
    root.title("InoDAQV2")

    panel_dig()
    panel_pwm()
    panel_analog_read()
    panel_digital_read()
    panel_tone()

    root.mainloop()


if __name__ == "__main__":
    main()
