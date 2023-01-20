from pytest import mark
from src.py.serial_connection import SerialConnection

def test_command_hello(connection: SerialConnection) -> None:

    connection.send_message('hello')
    status, returned_msg = connection.receive_message()

    assert status
    assert returned_msg == 'Hello from InoDAQV2'

PAIRS_PING = [
    ('ping', 'Built in LED is ON'),
    ('ping', 'Built in LED is OFF')
]

@mark.parametrize('command, expected_msg', PAIRS_PING)
def test_command_ping(connection: SerialConnection, command: str, expected_msg: str) -> None:

    connection.send_message(command)
    status, returned_msg = connection.receive_message()

    assert status
    assert returned_msg == expected_msg

PAIRS_DIG_1 = [
    ('dig', 'Unknown command: dig'),
    ('dig:', 'Malformed command. Missing second colon!'),
    ('dig:2', 'Malformed command. Missing second colon!'),
    ('dig:2:', "Valid states are 'on' and 'off'"),
    ('dig:2:foo', "Valid states are 'on' and 'off'"),
    ('dig:a:on', 'Malformed command. Could not parse digital pin!'),
    ('dig:-100:on', 'Must select a digital pin between 2 and 13!'),
    ('dig:1:on', 'Must select a digital pin between 2 and 13!'),
    ('dig:14:on', 'Must select a digital pin between 2 and 13!')
]

@mark.parametrize('command, expected_msg', PAIRS_DIG_1)
def test_command_dig_1(connection: SerialConnection, command: str, expected_msg: str) -> None:

    connection.send_message(command)
    status, returned_msg = connection.receive_message()

    assert not status
    assert returned_msg == expected_msg

PAIRS_DIG_2 = [
    ('dig:2:on', 'Pin 2 set to on'),
    ('dig:3:on', 'Pin 3 set to on'),
    ('dig:4:on', 'Pin 4 set to on'),
    ('dig:5:on', 'Pin 5 set to on'),
    ('dig:6:on', 'Pin 6 set to on'),
    ('dig:7:on', 'Pin 7 set to on'),
    ('dig:8:on', 'Pin 8 set to on'),
    ('dig:9:on', 'Pin 9 set to on'),
    ('dig:10:on', 'Pin 10 set to on'),
    ('dig:11:on', 'Pin 11 set to on'),
    ('dig:12:on', 'Pin 12 set to on'),
    ('dig:13:on', 'Pin 13 set to on'),
    ('dig:2:off', 'Pin 2 set to off'),
    ('dig:3:off', 'Pin 3 set to off'),
    ('dig:4:off', 'Pin 4 set to off'),
    ('dig:5:off', 'Pin 5 set to off'),
    ('dig:6:off', 'Pin 6 set to off'),
    ('dig:7:off', 'Pin 7 set to off'),
    ('dig:8:off', 'Pin 8 set to off'),
    ('dig:9:off', 'Pin 9 set to off'),
    ('dig:10:off', 'Pin 10 set to off'),
    ('dig:11:off', 'Pin 11 set to off'),
    ('dig:12:off', 'Pin 12 set to off'),
    ('dig:13:off', 'Pin 13 set to off')
]

@mark.parametrize('command, expected_msg', PAIRS_DIG_2)
def test_command_dig_2(connection: SerialConnection, command: str, expected_msg: str) -> None:

    connection.send_message(command)
    status, returned_msg = connection.receive_message()

    assert status
    assert returned_msg == expected_msg

PAIRS_PWM_1 = [
    ('pwm', 'Unknown command: pwm'),
    ('pwm:', 'Malformed command. Missing second colon!'),
    ('pwm:3', 'Malformed command. Missing second colon!'),
    ('pwm:a:', 'Malformed command. Could not parse digital pin!'),
    ('pwm:-2:', 'Digital pin must be one of 3, 5, 6, 9, 10 or 11'),
    ('pwm:2:', 'Digital pin must be one of 3, 5, 6, 9, 10 or 11'),
    ('pwm:3:a', 'Could not parse duty cycle!'),
    ('pwm:3:-100', 'Duty cycle must be between 0 and 255'),
    ('pwm:3:256', 'Duty cycle must be between 0 and 255'),
]

@mark.parametrize('command, expected_msg', PAIRS_PWM_1)
def test_command_pwm_1(connection: SerialConnection, command: str, expected_msg: str) -> None:

    connection.send_message(command)
    status, returned_msg = connection.receive_message()

    assert not status
    assert returned_msg == expected_msg

PAIRS_PWM_2 = [
    ('pwm:3:0', 'Pin 3 emitting PWM wave with duty cycle of 0'),
    ('pwm:5:0', 'Pin 5 emitting PWM wave with duty cycle of 0'),
    ('pwm:6:0', 'Pin 6 emitting PWM wave with duty cycle of 0'),
    ('pwm:9:0', 'Pin 9 emitting PWM wave with duty cycle of 0'),
    ('pwm:10:0', 'Pin 10 emitting PWM wave with duty cycle of 0'),
    ('pwm:11:0', 'Pin 11 emitting PWM wave with duty cycle of 0'),
    ('pwm:3:255', 'Pin 3 emitting PWM wave with duty cycle of 255'),
    ('pwm:5:255', 'Pin 5 emitting PWM wave with duty cycle of 255'),
    ('pwm:6:255', 'Pin 6 emitting PWM wave with duty cycle of 255'),
    ('pwm:9:255', 'Pin 9 emitting PWM wave with duty cycle of 255'),
    ('pwm:10:255', 'Pin 10 emitting PWM wave with duty cycle of 255'),
    ('pwm:11:255', 'Pin 11 emitting PWM wave with duty cycle of 255')
]

@mark.parametrize('command, expected_msg', PAIRS_PWM_2)
def test_command_pwm_2(connection: SerialConnection, command: str, expected_msg: str) -> None:

    connection.send_message(command)
    status, returned_msg = connection.receive_message()

    assert status
    assert returned_msg == expected_msg
