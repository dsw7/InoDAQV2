from tkinter import Tk
from serial_connection import SerialConnection
from user_interface import PanelDig, PanelPWM

def main() -> None:

    with SerialConnection() as connection:
        root = Tk()
        root.title('InoDAQV2')
        root.geometry('1200x300')

        PanelDig(root, connection)
        PanelPWM(root)
        root.mainloop()

if __name__ == '__main__':
    main()
