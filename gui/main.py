import sys
from tkinter import Tk, _tkinter

try:
    root = Tk()
except _tkinter.TclError as exception:
    sys.exit(f'Missing X11 graphic layer: "{exception}"')

from gui.frame_analog_read import frame_analog_read
from gui.frame_digital_pins import frame_digital_pins
from gui.frame_digital_read import frame_digital_read
from gui.frame_pwm import frame_pwm
from gui.frame_tone import frame_tone
from gui.menu import menu


def main() -> None:
    root.title("InoDAQV2")

    menu(root)
    frame_digital_pins(root)
    frame_pwm(root)
    frame_analog_read(root)
    frame_digital_read(root)
    frame_tone(root)

    root.mainloop()


if __name__ == "__main__":
    main()
