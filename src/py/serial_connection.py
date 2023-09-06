import sys
from logging import getLogger
from time import sleep
from json import dumps
from typing import Tuple, TypeVar
from configparser import SectionProxy
import serial

T = TypeVar("T")


class SerialConnection:
    logger = getLogger("inodaqv2")

    def __init__(self: T, configs: SectionProxy) -> T:
        self.configs = configs
        self.serial_port_obj = None

    def __enter__(self: T) -> T:
        connection_params = {
            "baudrate": self.configs["baud"],
            "parity": serial.PARITY_NONE,
            "stopbits": serial.STOPBITS_ONE,
            "bytesize": serial.EIGHTBITS,
            "timeout": self.configs.getfloat("timeout"),
            "port": self.configs["port"],
        }

        self.logger.info(
            "Connecting using parameters:\n%s", dumps(connection_params, indent=4)
        )

        try:
            self.serial_port_obj = serial.Serial(**connection_params)
        except serial.serialutil.SerialException as exception:
            sys.exit(f'An exception occurred when connecting: "{exception}"')

        if not self.serial_port_obj.is_open:
            sys.exit(f'Could not connect to "{self.serial_port_obj.name}"')

        # Opening a connection will send a DTR (Data Terminal Ready) signal to device, which will
        # force the device to reset. Give device 2 seconds to reset

        self.logger.info(
            "DTR (Data Terminal Ready) was sent. Waiting for device to reset"
        )
        sleep(2)

        self.logger.info("Device ready to accept instructions!")

        self.send_message("hello")
        status, message = self.receive_message()

        if not status:
            sys.exit(f"Failed to connect on handshake: {message}")

        if message != "Hello from InoDAQV2":
            sys.exit(
                "Handshake returned unrecognized message. Is the right code uploaded to device?"
            )

        return self

    def __exit__(self: T, *args) -> None:
        if self.serial_port_obj is None:
            self.logger.info("Not closing connection. Connection was never opened!")
            return

        self.logger.info("Closing connection!")

        if self.serial_port_obj.is_open:
            self.send_message("exit")
            self.receive_message()
            self.serial_port_obj.close()

    def send_message(self: T, message: str) -> None:
        self.logger.debug('Sending message: "%s"', message)
        message = message.encode(encoding=self.configs["encoding"])

        self.logger.debug("Sent %i bytes", self.serial_port_obj.write(message))
        self.serial_port_obj.flush()

    def receive_message(self: T) -> Tuple[bool, str]:
        self.logger.debug("Waiting to receive message...")
        message_received = False

        while not message_received:
            while self.serial_port_obj.in_waiting < 1:
                pass

            bytes_from_dev = (
                self.serial_port_obj.read_until()
            )  # Reads until \n by default
            message_received = True

        if len(bytes_from_dev) > 80:
            self.logger.debug("Received message: %s...", bytes_from_dev[:80])
            self.logger.debug("Message was truncated due to excessive length")
        else:
            self.logger.debug("Received message: %s", bytes_from_dev)

        try:
            results = bytes_from_dev.decode(self.configs["encoding"]).strip()
        except UnicodeDecodeError as e:
            return False, f'An exception occurred when decoding results: "{e}"'

        status, message = results.split(";")

        return int(status) == 1, message
