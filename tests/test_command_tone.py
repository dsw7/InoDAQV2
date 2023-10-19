from pytest import mark
from inoio import InoIO

PAIRS_TONE_1 = [
    ("tone", "0;Unknown command: tone"),
    ("tone:", "0;Malformed command. Missing second colon!"),
    ("tone:2", "0;Malformed command. Missing second colon!"),
    ("tone:a:", "0;Malformed command. Could not parse digital pin!"),
    ("tone:-2:", "0;Tone pin must be one of 2, 4, 7 or 8"),
    ("tone:2:", "0;Malformed command. Could not parse frequency!"),
    ("tone:2:a", "0;Malformed command. Could not parse frequency!"),
    ("tone:2:-100", "0;Frequency must be between 31 and 65535 Hz"),
    ("tone:2:100000", "0;Frequency must be between 31 and 65535 Hz"),
]


@mark.parametrize("command, expected_msg", PAIRS_TONE_1)
def test_command_tone_invalid_commands(
    connection: InoIO, command: str, expected_msg: str
) -> None:
    connection.write(command)
    assert expected_msg == connection.read()


PAIRS_TONE_2 = [
    ("tone:2:31", "1;2,31"),
    ("tone:4:33", "1;4,33"),
    ("tone:7:36", "1;7,36"),
    ("tone:8:37", "1;8,37"),
]


@mark.parametrize("command, expected_msg", PAIRS_TONE_2)
def test_command_tone_valid(connection: InoIO, command: str, expected_msg: str) -> None:
    connection.write(command)
    assert expected_msg == connection.read()


PAIRS_TONE_3 = [
    ("tone:3:32", "0;Tone pin must be one of 2, 4, 7 or 8"),
    ("tone:5:34", "0;Tone pin must be one of 2, 4, 7 or 8"),
    ("tone:6:35", "0;Tone pin must be one of 2, 4, 7 or 8"),
    ("tone:9:38", "0;Tone pin must be one of 2, 4, 7 or 8"),
    ("tone:10:39", "0;Tone pin must be one of 2, 4, 7 or 8"),
    ("tone:11:40", "0;Tone pin must be one of 2, 4, 7 or 8"),
    ("tone:12:41", "0;Tone pin must be one of 2, 4, 7 or 8"),
    ("tone:13:42", "0;Tone pin must be one of 2, 4, 7 or 8"),
]


@mark.parametrize("command, expected_msg", PAIRS_TONE_3)
def test_command_tone_invalid_pins(
    connection: InoIO, command: str, expected_msg: str
) -> None:
    connection.write(command)
    assert expected_msg == connection.read()


def test_command_tone_dig(connection: InoIO) -> None:
    # Ensure that we can still set a dig after a tone and vice versa

    connection.write("tone:2:100")
    connection.read()

    connection.write("dig:2:on")
    assert connection.read() == "1;2,on"

    connection.write("tone:2:100")
    assert connection.read() == "1;2,100"
