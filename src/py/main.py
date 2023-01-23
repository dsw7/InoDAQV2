import logging
from tkinter import Tk
from serial_connection import SerialConnection
from user_interface import PanelDig, PanelPWM

def setup_logger() -> None:

    logger = logging.getLogger('inodaq')
    logger.setLevel(logging.INFO)

    stream = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt='%(asctime)s.%(msecs)03d %(message)s',
        datefmt='%Y-%m-%d %I:%M:%S'
    )
    stream.setFormatter(formatter)

    logger.addHandler(stream)

def main() -> None:
    setup_logger()

    with SerialConnection() as connection:
        root = Tk()
        root.title('InoDAQV2')
        root.geometry('1200x300')

        PanelDig(root, connection)
        PanelPWM(root)
        root.mainloop()

if __name__ == '__main__':
    main()
