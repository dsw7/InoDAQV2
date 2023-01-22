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
        self.position = 3
        self.toggled = False

    def cursor_up(self: T) -> None:
        self.position -= 1

        if self.position < 3:
            self.position = 14

    def cursor_down(self: T) -> None:
        self.position += 1

        if self.position > 14:
            self.position = 3

    def toggle_pin(self: T) -> None:
        self.toggled = not self.toggled

    def dig_command_panel(self: T) -> None:

        self.stdscr.hline(0, 0, '-', C.columns)
        self.stdscr.addstr(1, C.col_a, 'Toggle digital pins', curses.A_BOLD + curses.A_UNDERLINE)

        for idx in range(3, 15):

            if idx == self.position:
                mode = curses.A_REVERSE
            else:
                mode = curses.A_NORMAL

            self.stdscr.addstr(idx, C.col_a, f'Pin {idx - 1}', mode)
            self.stdscr.addstr(idx, C.col_b, '[ ]', mode)

    def event_loop(self: T) -> None:

        self.dig_command_panel()
        key_input = None

        while key_input != ord('q'):
            key_input = self.stdscr.getch()

            if key_input == curses.KEY_UP:
                self.cursor_up()
            elif key_input == curses.KEY_DOWN:
                self.cursor_down()
            elif key_input == curses.KEY_ENTER:
                self.toggle_pin()

            self.dig_command_panel()
            self.stdscr.refresh()


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
