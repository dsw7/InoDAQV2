from pytest import mark
from inoio import InoIO

PAIRS_PING = [("ping", "Built in LED is ON"), ("ping", "Built in LED is OFF")]


@mark.parametrize("command, expected_msg", PAIRS_PING)
def test_command_ping(connection: InoIO, command: str, expected_msg: str) -> None:
    connection.write(command)
    msg = connection.read()

    status, returned_msg = msg.split(";")
    assert int(status) == 1
    assert returned_msg == expected_msg
