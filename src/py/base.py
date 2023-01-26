from logging import getLogger
from abc import ABC, abstractmethod
from typing import TypeVar
from tkinter import Tk
from serial_connection import SerialConnection

T = TypeVar('T')


class PanelBase(ABC):

    logger = getLogger('inodaqv2')

    kw_labelframe = {
        'side': 'left', 'fill': 'both', 'expand': True, 'padx': 5, 'pady': 5, 'ipady': 3, 'ipadx': 3
    }

    def __init__(self: T, root: Tk, connection: SerialConnection) -> T:

        self.root = root
        self.connection = connection
        self.pins = {}
        self.setup_panel()

    @abstractmethod
    def setup_panel(self: T) -> None:
        pass

    @abstractmethod
    def toggle(self: T, pin: int) -> None:
        pass
