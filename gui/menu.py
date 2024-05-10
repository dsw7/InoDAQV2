from tkinter import Tk, StringVar, Menu
from inoio import errors
from serial.tools import list_ports
from gui.consts import LOGGER
from gui.extensions import conn

_SERIAL_PORT = StringVar()


def connect_on_port() -> None:
    conn.init_app(port=_SERIAL_PORT.get())

    try:
        conn.connect()
    except errors.InoIOConnectionError as e:
        raise ConnectionError("Could not connect to device") from e

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


def menu(root: Tk) -> None:
    menu_bar = Menu(root)
    menu_port = Menu(menu_bar, tearoff=0)

    for port in list_ports.comports():
        menu_port.add_radiobutton(
            label=port.device,
            value=port.device,
            variable=_SERIAL_PORT,
            command=connect_on_port,
        )

    menu_bar.add_cascade(label="Port", menu=menu_port)

    root.config(menu=menu_bar)
