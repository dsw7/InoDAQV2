import sys
import typing
import curses
from serial_connection import SerialConnection

T = typing.TypeVar('T')
MIN_COLUMNS = 150
MIN_ROWS = 25


class MainPanel:

    def __init__(self: T, stdscr: curses.window, connection: SerialConnection) -> T:

        self.stdscr = stdscr
        self.connection = connection

    def event_loop(self: T) -> None:
        self.stdscr.getch()


def main(stdscr: curses.window) -> None:

    curses.curs_set(0)
    rows, columns = stdscr.getmaxyx()

    if columns < MIN_COLUMNS:
        sys.exit('Terminal is not wide enough!')

    if rows < MIN_ROWS:
        sys.exit('Terminal is not tall enough!')

    with SerialConnection() as connection:
        MainPanel(stdscr, connection).event_loop()

if __name__ == '__main__':
    curses.wrapper(main)
