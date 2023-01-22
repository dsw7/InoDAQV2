import sys
import typing
import curses
from dataclasses import dataclass
from serial_connection import SerialConnection

T = typing.TypeVar('T')
MIN_COLUMNS = 150
MIN_ROWS = 25

@dataclass
class C:

    columns: int = 0
    rows: int = 0

    col_a: int = 1
    col_b: int = 11
    col_c: int = 21


class MainPanel:

    def __init__(self: T, stdscr: curses.window, connection: SerialConnection) -> T:

        self.stdscr = stdscr
        self.connection = connection

    def dig_command_panel(self: T) -> None:

        self.stdscr.hline(0, 0, '-', C.columns)
        self.stdscr.addstr(1, C.col_a, 'Toggle digital pins 2-13', curses.A_BOLD + curses.A_UNDERLINE)

        for c in range(3, 15):
            self.stdscr.addstr(c, C.col_a, f'{c - 1}')
            self.stdscr.addstr(c, C.col_b, '[ ]')

    def event_loop(self: T) -> None:
        self.dig_command_panel()
        self.stdscr.getch()


def main(stdscr: curses.window) -> None:

    curses.curs_set(0)
    rows, columns = stdscr.getmaxyx()

    if columns < MIN_COLUMNS:
        sys.exit('Terminal is not wide enough!')

    if rows < MIN_ROWS:
        sys.exit('Terminal is not tall enough!')

    C.columns = columns
    C.rows = rows

    with SerialConnection() as connection:
        MainPanel(stdscr, connection).event_loop()

if __name__ == '__main__':
    curses.wrapper(main)
