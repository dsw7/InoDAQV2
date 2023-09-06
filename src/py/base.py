from logging import getLogger
from abc import ABC, abstractmethod
from tkinter import Tk
from serial_connection import SerialConnection


class PanelBase(ABC):
    logger = getLogger("inodaqv2")

    kw_labelframe = {
        "side": "left",
        "fill": "both",
        "expand": True,
        "padx": 5,
        "pady": 5,
        "ipady": 3,
        "ipadx": 3,
    }

    def __init__(self, root: Tk, connection: SerialConnection) -> None:
        self.root = root
        self.connection = connection
        self.pins = {}
        self.setup_panel()

    @abstractmethod
    def setup_panel(self) -> None:
        pass
