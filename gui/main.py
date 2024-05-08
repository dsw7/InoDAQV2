import sys
from inoio import errors
from gui import actions
from gui.extensions import conn


def run_test() -> None:

    print(actions.toggle_digital_pins(pin=2, state=True))
    print(actions.read_analog_pins())
    print(actions.read_digital_pins())
    print(actions.set_pwm(pin=3, duty_cycle=50))
    print(actions.set_tone(pin=4, frequency="25"))


def main() -> None:
    serial_port = sys.argv[1]
    conn.init_app(port=serial_port)

    try:
        conn.connect()
    except errors.InoIOConnectionError as e:
        sys.exit(e)

    try:
        actions.run_handshake()
    except ConnectionError as e:
        sys.exit(str(e))

    run_test()


if __name__ == "__main__":
    main()
