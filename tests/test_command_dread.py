from inodaqv2.serial_connection import SerialConnection


def test_command_dread(connection: SerialConnection) -> None:
    connection.send_message("dread")
    status, returned_msg = connection.receive_message()

    assert status

    for val in returned_msg.split(","):
        assert 0 <= int(val) <= 1023
