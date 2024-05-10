from re import match
from pytest import mark
from inoio import InoIO
from gui.consts import PAT_VALID_PWM

PAIRS_PWM_1 = [
    ("pwm", "0;Unknown command: pwm"),
    ("pwm:", "0;Malformed command. Missing second colon!"),
    ("pwm:3", "0;Malformed command. Missing second colon!"),
    ("pwm:a:", "0;Malformed command. Could not parse digital pin!"),
    ("pwm:-2:", "0;Digital pin must be one of 3, 5, 6, 9, 10 or 11"),
    ("pwm:2:", "0;Digital pin must be one of 3, 5, 6, 9, 10 or 11"),
    ("pwm:3:a", "0;Could not parse duty cycle!"),
    ("pwm:3:-100", "0;Duty cycle must be between 0 and 255"),
    ("pwm:3:256", "0;Duty cycle must be between 0 and 255"),
]


@mark.parametrize("command, expected_msg", PAIRS_PWM_1)
def test_command_pwm_invalid(
    connection: InoIO, command: str, expected_msg: str
) -> None:
    connection.write(command)
    assert expected_msg == connection.read()


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
def test_command_dig_valid(connection: InoIO, command: str, expected_msg: str) -> None:
    connection.write(command)
    reply = connection.read()

    assert expected_msg == reply
    assert match(PAT_VALID_PWM, reply) is not None


INVALID_REPLIES = [
    "0;3,255",
    "1;333,255",
    "1;3,2555",
    "1;3,",
    "1;3,255,255",
]


@mark.parametrize("reply", INVALID_REPLIES)
def test_regex_invalid_reply(reply: str) -> None:
    assert match(PAT_VALID_PWM, reply) is None
