from re import match
from pytest import mark
from inoio import InoIO
from inodaqv2.components.actions import PAT_VALID_DIG

PAIRS_DIG_1 = [
    ("dig", "0;Unknown command: dig"),
    ("dig:", "0;Malformed command. Missing second colon!"),
    ("dig:2", "0;Malformed command. Missing second colon!"),
    ("dig:2:", "0;Valid states are 'on' and 'off'"),
    ("dig:2:foo", "0;Valid states are 'on' and 'off'"),
    ("dig:a:on", "0;Malformed command. Could not parse digital pin!"),
    ("dig:-100:on", "0;Must select a digital pin between 2 and 13!"),
    ("dig:1:on", "0;Must select a digital pin between 2 and 13!"),
    ("dig:14:on", "0;Must select a digital pin between 2 and 13!"),
]


@mark.parametrize("command, expected_msg", PAIRS_DIG_1)
def test_command_dig_invalid(
    connection: InoIO, command: str, expected_msg: str
) -> None:
    connection.write(command)
    assert expected_msg == connection.read()


PAIRS_DIG_2 = [
    ("dig:2:on", "1;2,on"),
    ("dig:3:on", "1;3,on"),
    ("dig:4:on", "1;4,on"),
    ("dig:5:on", "1;5,on"),
    ("dig:6:on", "1;6,on"),
    ("dig:7:on", "1;7,on"),
    ("dig:8:on", "1;8,on"),
    ("dig:9:on", "1;9,on"),
    ("dig:10:on", "1;10,on"),
    ("dig:11:on", "1;11,on"),
    ("dig:12:on", "1;12,on"),
    ("dig:13:on", "1;13,on"),
    ("dig:2:off", "1;2,off"),
    ("dig:3:off", "1;3,off"),
    ("dig:4:off", "1;4,off"),
    ("dig:5:off", "1;5,off"),
    ("dig:6:off", "1;6,off"),
    ("dig:7:off", "1;7,off"),
    ("dig:8:off", "1;8,off"),
    ("dig:9:off", "1;9,off"),
    ("dig:10:off", "1;10,off"),
    ("dig:11:off", "1;11,off"),
    ("dig:12:off", "1;12,off"),
    ("dig:13:off", "1;13,off"),
]


@mark.parametrize("command, expected_msg", PAIRS_DIG_2)
def test_command_dig_valid(connection: InoIO, command: str, expected_msg: str) -> None:
    connection.write(command)
    reply = connection.read()

    assert expected_msg == reply
    assert match(PAT_VALID_DIG, reply) is not None


INVALID_REPLIES = [
    ("0;13,off"),
    ("1;133,off"),
    ("1;abc,off"),
    ("1;13,of"),
    ("1;13,offf"),
    ("1;13,off,on"),
]


@mark.parametrize("reply", INVALID_REPLIES)
def test_regex_invalid_reply(reply: str) -> None:
    assert match(PAT_VALID_DIG, reply) is None
