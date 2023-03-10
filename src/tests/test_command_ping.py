from pytest import mark
from src.py.serial_connection import SerialConnection

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
