import sys
from tkinter import Tk, ttk, _tkinter
from inoio import errors
from gui import actions
from gui.extensions import conn

try:
    root = Tk()
except _tkinter.TclError as exception:
    sys.exit(f'Missing X11 graphic layer: "{exception}"')

from gui.frame_digital_pins import frame_digital_pins
from gui.frame_pwm import frame_pwm
from gui.frame_analog_read import frame_analog_read


def panel_digital_read() -> None:
    frame = ttk.LabelFrame(root, padding=10, text="Digital Read")
    frame.grid(row=0, column=3, sticky="ns", padx=2)

    ttk.Button(frame, text="Quit", command=root.destroy).grid(column=1, row=0)
    ttk.Button(frame, text="Quit", command=root.destroy).grid(column=1, row=1)


def panel_tone() -> None:
    frame = ttk.LabelFrame(root, padding=10, text="Tone")
    frame.grid(row=0, column=4, sticky="ns", padx=2)

    ttk.Button(frame, text="Quit", command=root.destroy).grid(column=1, row=0)


def run_test() -> None:

    print(actions.read_digital_pins())
    print(actions.set_tone(pin=4, frequency="25"))


def main() -> None:
    serial_port = sys.argv[1]
    conn.init_app(port=serial_port)

    try:
        conn.connect()
    except errors.InoIOConnectionError as e:
        sys.exit(e)

    try:
        actions.run_handshake()
    except ConnectionError as e:
        sys.exit(str(e))

    root.title("InoDAQV2")

    frame_digital_pins(root)
    frame_pwm(root)
    frame_analog_read(root)
    panel_digital_read()
    panel_tone()

    root.mainloop()


if __name__ == "__main__":
    main()
