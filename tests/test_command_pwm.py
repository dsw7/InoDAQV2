from pytest import mark
from inoio import InoIO

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
def test_command_pwm_1(connection: InoIO, command: str, expected_msg: str) -> None:
    connection.write(command)

    msg = connection.read()
    status, returned_msg = msg.split(";")

    assert int(status) == 0
    assert returned_msg == expected_msg


PAIRS_PWM_2 = [
    ("pwm:3:0", "1;3,0"),
    ("pwm:5:0", "1;5,0"),
    ("pwm:6:0", "1;6,0"),
    ("pwm:9:0", "1;9,0"),
    ("pwm:10:0", "1;10,0"),
    ("pwm:11:0", "1;11,0"),
    ("pwm:3:255", "1;3,255"),
    ("pwm:5:255", "1;5,255"),
    ("pwm:6:255", "1;6,255"),
    ("pwm:9:255", "1;9,255"),
    ("pwm:10:255", "1;10,255"),
    ("pwm:11:255", "1;11,255"),
]


@mark.parametrize("command, expected_msg", PAIRS_PWM_2)
def test_command_pwm_2(connection: InoIO, command: str, expected_msg: str) -> None:
    connection.write(command)
    assert expected_msg == connection.read()
