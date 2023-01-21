import sys
import typing
import curses

T = typing.TypeVar('T')
MIN_COLUMNS = 150
MIN_ROWS = 25


class MainPanel:

    def __init__(self: T, stdscr: curses.window) -> T:
        self.stdscr = stdscr

    def event_loop(self: T) -> None:
        self.stdscr.getch()


def main(stdscr: curses.window) -> None:

    curses.curs_set(0)
    rows, columns = stdscr.getmaxyx()

    if columns < MIN_COLUMNS:
        sys.exit('Terminal is not wide enough!')

    if rows < MIN_ROWS:
        sys.exit('Terminal is not tall enough!')

    MainPanel(stdscr).event_loop()

if __name__ == '__main__':
    curses.wrapper(main)
