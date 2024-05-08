from re import match
from inoio import InoIO
from pytest import mark
from gui.actions import PAT_VALID_AREAD


def test_command_aread(connection: InoIO) -> None:
    connection.write("aread")
    assert match(PAT_VALID_AREAD, connection.read()) is not None


INVALID_REPLIES = [
    "0;100,200,300,400,500,600",
    "1;100,200,300,400,500,",
    "1;100,200,300,400,500,10233",
    "1;abc,200,300,400,500,600",
]


@mark.parametrize("reply", INVALID_REPLIES)
def test_regex_invalid_reply(reply: str) -> None:
    assert match(PAT_VALID_AREAD, reply) is None
