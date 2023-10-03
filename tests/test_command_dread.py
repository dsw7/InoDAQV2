from re import match
from inoio import InoIO
from pytest import mark
from inodaqv2.components.actions import PAT_VALID_DREAD


def test_command_dread(connection: InoIO) -> None:
    connection.write("dread")
    assert match(PAT_VALID_DREAD, connection.read()) is not None


INVALID_REPLIES = [
    "0;0,0,0,0,0,0",
    "1;0,0,0,0,0,",
    "1;0,0,0,0,0,10",
    "1;a,b,0,0,0,1",
    "1;0,0,0,0,0,0,0",
]


@mark.parametrize("reply", INVALID_REPLIES)
def test_regex_invalid_reply(reply: str) -> None:
    assert match(PAT_VALID_DREAD, reply) is None
