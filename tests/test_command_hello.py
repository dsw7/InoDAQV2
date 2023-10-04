from inoio import InoIO


def test_command_hello(connection: InoIO) -> None:
    connection.write("hello")
    msg = connection.read()

    status, returned_msg = msg.split(";")
    assert int(status) == 1
    assert returned_msg == "Hello from InoDAQV2"
