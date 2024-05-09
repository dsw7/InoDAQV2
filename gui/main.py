import sys
from tkinter import Tk, _tkinter
from inoio import errors
from gui.consts import LOGGER
from gui.extensions import conn

try:
    root = Tk()
except _tkinter.TclError as exception:
    sys.exit(f'Missing X11 graphic layer: "{exception}"')

from gui.frame_digital_pins import frame_digital_pins
from gui.frame_pwm import frame_pwm
from gui.frame_analog_read import frame_analog_read
from gui.frame_digital_read import frame_digital_read
from gui.frame_tone import frame_tone


def run_handshake() -> None:
    LOGGER.info("Handshaking with device")
    LOGGER.info('Sending command: "hello"')

    try:
        conn.write("hello")
    except errors.InoIOTransmissionError as e:
        LOGGER.exception("Failed to send command")
        raise ConnectionError("Could not connect to device") from e

    reply = conn.read()

    if reply != "1;Hello from InoDAQV2":
        LOGGER.error('Handshake returned unknown message: "%s"', reply)
        raise ConnectionError("Handshake returned unknown message")


def main() -> None:
    serial_port = sys.argv[1]
    conn.init_app(port=serial_port)

    try:
        conn.connect()
    except errors.InoIOConnectionError as e:
        sys.exit(e)

    try:
        run_handshake()
    except ConnectionError as e:
        sys.exit(str(e))

    root.title("InoDAQV2")

    frame_digital_pins(root)
    frame_pwm(root)
    frame_analog_read(root)
    frame_digital_read(root)
    frame_tone(root)

    root.mainloop()


if __name__ == "__main__":
    main()
