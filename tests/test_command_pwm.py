from pytest import mark
from inodaqv2.serial_connection import SerialConnection

PAIRS_PWM_1 = [
    ("pwm", "Unknown command: pwm"),
    ("pwm:", "Malformed command. Missing second colon!"),
    ("pwm:3", "Malformed command. Missing second colon!"),
    ("pwm:a:", "Malformed command. Could not parse digital pin!"),
    ("pwm:-2:", "Digital pin must be one of 3, 5, 6, 9, 10 or 11"),
    ("pwm:2:", "Digital pin must be one of 3, 5, 6, 9, 10 or 11"),
    ("pwm:3:a", "Could not parse duty cycle!"),
    ("pwm:3:-100", "Duty cycle must be between 0 and 255"),
    ("pwm:3:256", "Duty cycle must be between 0 and 255"),
]


@mark.parametrize("command, expected_msg", PAIRS_PWM_1)
def test_command_pwm_1(
    connection: SerialConnection, command: str, expected_msg: str
) -> None:
    connection.send_message(command)
    status, returned_msg = connection.receive_message()

    assert not status
    assert returned_msg == expected_msg


PAIRS_PWM_2 = [
    ("pwm:3:0", "Pin 3 emitting PWM wave with duty cycle of 0"),
    ("pwm:5:0", "Pin 5 emitting PWM wave with duty cycle of 0"),
    ("pwm:6:0", "Pin 6 emitting PWM wave with duty cycle of 0"),
    ("pwm:9:0", "Pin 9 emitting PWM wave with duty cycle of 0"),
    ("pwm:10:0", "Pin 10 emitting PWM wave with duty cycle of 0"),
    ("pwm:11:0", "Pin 11 emitting PWM wave with duty cycle of 0"),
    ("pwm:3:255", "Pin 3 emitting PWM wave with duty cycle of 255"),
    ("pwm:5:255", "Pin 5 emitting PWM wave with duty cycle of 255"),
    ("pwm:6:255", "Pin 6 emitting PWM wave with duty cycle of 255"),
    ("pwm:9:255", "Pin 9 emitting PWM wave with duty cycle of 255"),
    ("pwm:10:255", "Pin 10 emitting PWM wave with duty cycle of 255"),
    ("pwm:11:255", "Pin 11 emitting PWM wave with duty cycle of 255"),
]


@mark.parametrize("command, expected_msg", PAIRS_PWM_2)
def test_command_pwm_2(
    connection: SerialConnection, command: str, expected_msg: str
) -> None:
    connection.send_message(command)
    status, returned_msg = connection.receive_message()

    assert status
    assert returned_msg == expected_msg
