import sys
from inoio import errors
from gui import actions
from gui.extensions import conn


def run_test() -> None:

    print(actions.toggle_digital_pins(pin=2, state=True))
    print(actions.read_analog_pins())
    print(actions.read_digital_pins())

    """
    if payload["action"] == "pwm":
        print(actions.set_pwm(payload["pin"], payload["value"]))

    if payload["action"] == "tone":
        print(actions.set_tone(payload["pin"], payload["frequency"]))
    """


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
