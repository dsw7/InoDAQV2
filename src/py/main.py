import sys
import logging
from pathlib import Path
from tkinter import Tk, _tkinter
from configparser import ConfigParser
from serial_connection import SerialConnection
from user_interface import PanelDig, PanelPWM

def read_ini() -> ConfigParser:

    path_ini = Path(__file__).parents[1] / 'configs/inodaqv2.ini'

    if not path_ini.exists():
        sys.exit(f'Path "{path_ini}" does not exist')

    configs = ConfigParser()
    configs.read(path_ini)

    return configs

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

    configs = read_ini()
    setup_logger()

    try:
        root = Tk()
    except _tkinter.TclError as exception:
        sys.exit(f'Missing X11 graphic layer: "{exception}"')

    root.title('InoDAQV2')

    with SerialConnection(configs['connection']) as connection:
        PanelDig(root, connection)
        PanelPWM(root)
        root.mainloop()

if __name__ == '__main__':
    main()
