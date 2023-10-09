from pytest import mark
from inoio import InoIO

PAIRS_TONE_1 = [
    ("tone", "0;Unknown command: tone"),
    ("tone:", "0;Malformed command. Missing second colon!"),
    ("tone:3", "0;Malformed command. Missing second colon!"),
    ("tone:a:", "0;Malformed command. Could not parse digital pin!"),
    ("tone:-2:", "0;Must select a digital pin between 2 and 13!"),
    ("tone:2:", "0;Malformed command. Could not parse frequency!"),
    ("tone:3:a", "0;Malformed command. Could not parse frequency!"),
    ("tone:3:-100", "0;Frequency must be between 31 and 65535 Hz"),
    ("tone:3:100000", "0;Frequency must be between 31 and 65535 Hz"),
]


@mark.parametrize("command, expected_msg", PAIRS_TONE_1)
def test_command_tone_invalid(
    connection: InoIO, command: str, expected_msg: str
) -> None:
    connection.write(command)
    assert expected_msg == connection.read()


PAIRS_TONE_2 = [
    ("tone:2:31", "1;2,31,-1"),
    ("tone:3:32", "1;3,32,2"),
    ("tone:4:33", "1;4,33,3"),
    ("tone:5:34", "1;5,34,4"),
    ("tone:6:35", "1;6,35,5"),
    ("tone:7:36", "1;7,36,6"),
    ("tone:8:37", "1;8,37,7"),
    ("tone:9:38", "1;9,38,8"),
    ("tone:10:39", "1;10,39,9"),
    ("tone:11:40", "1;11,40,10"),
    ("tone:12:41", "1;12,41,11"),
    ("tone:13:42", "1;13,42,12"),
]


@mark.parametrize("command, expected_msg", PAIRS_TONE_2)
def test_command_tone_valid(connection: InoIO, command: str, expected_msg: str) -> None:
    connection.write(command)
    assert expected_msg == connection.read()