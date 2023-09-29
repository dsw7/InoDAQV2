from inoio import InoIO


def test_command_aread(connection: InoIO) -> None:
    connection.write("aread")
    msg = connection.read()

    status, values = msg.split(";")
    assert int(status) == 1

    for val in values.split(","):
        assert 0 <= int(val) <= 1023
