from inodaqv2.serial_connection import SerialConnection


def test_command_hello(connection: SerialConnection) -> None:
    connection.send_message("hello")
    status, returned_msg = connection.receive_message()

    assert status
    assert returned_msg == "Hello from InoDAQV2"
