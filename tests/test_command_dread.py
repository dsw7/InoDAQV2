from inoio import InoIO


def test_command_dread(connection: InoIO) -> None:
    connection.write("dread")
    msg = connection.read()

    status, values = msg.split(";")
    assert int(status) == 1

    for val in values.split(","):
        assert 0 <= int(val) <= 1023
