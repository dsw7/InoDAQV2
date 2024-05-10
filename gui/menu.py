from tkinter import Tk, StringVar, Menu, messagebox
from inoio import errors
from serial.tools import list_ports
from gui.consts import LOGGER
from gui.extensions import conn

_SERIAL_PORT = StringVar()


def connect_on_port() -> None:
    port = _SERIAL_PORT.get()
    LOGGER.info("Connecting to %s", port)

    conn.init_app(port=port)

    try:
        conn.connect()
    except errors.InoIOConnectionError as e:
        LOGGER.exception("Could not connect to device")
        messagebox.showerror("Error", e)
        return

    LOGGER.info("Handshaking with device")
    LOGGER.info('Sending command: "hello"')

    try:
        conn.write("hello")
    except errors.InoIOTransmissionError as e:
        LOGGER.exception("Handshake with device failed")
        messagebox.showerror("Error", e)
        return

    reply = conn.read()

    if reply != "1;Hello from InoDAQV2":
        LOGGER.error('Handshake returned unknown message: "%s"', reply)
        messagebox.showerror("Error", "Handshake failure")
        return

    LOGGER.info("Handshake was successful. Ready to accept I/O!")


def disconnect_from_port() -> None:
    if not conn.is_connected:
        LOGGER.info("Nothing is connected")
        return

    LOGGER.info("Disconnecting from %s", conn.port)
    conn.disconnect()
    LOGGER.info("Disconnected")


def menu(root: Tk) -> None:
    menu_bar = Menu(root)
    menu_port = Menu(menu_bar, tearoff=0)

    ports = list_ports.comports()

    if not ports:
        menu_port.add_command(label="No ports available", state="disabled")
    else:
        for port in ports:
            menu_port.add_radiobutton(
                label=port.device,
                value=port.device,
                variable=_SERIAL_PORT,
                command=connect_on_port,
            )

        menu_port.add_separator()
        menu_port.add_command(label="Disconnect", command=disconnect_from_port)

    menu_bar.add_cascade(label="Port", menu=menu_port)
    root.config(menu=menu_bar)
