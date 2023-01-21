import sys
import logging
from time import sleep
from json import dumps
from typing import TypeVar, Tuple
from configparser import ConfigParser
from pathlib import Path
import serial

T = TypeVar('T')

def read_ini() -> ConfigParser:

    path_ini = Path(__file__).parent / 'inodaqv2.ini'

    if not path_ini.exists():
        sys.exit(f'Path "{path_ini}" does not exist')

    configs = ConfigParser()
    configs.read(path_ini)

    return configs


class SerialConnection:

    def __init__(self: T) -> T:

        self.configs = read_ini()
        self.serial_port_obj = None

        if self.configs['logging'].getboolean('debug'):
            level = logging.DEBUG
        else:
            level = logging.INFO

        configs = {
            'level': level,
            'format': '%(asctime)s.%(msecs)03d %(message)s',
            'datefmt': '%Y-%m-%d %I:%M:%S'
        }

        logging.basicConfig(**configs)
        self.logger = logging.getLogger(__class__.__name__)

    def __enter__(self: T) -> T:

        connection_params = {
            'baudrate': self.configs['connection']['baud'],
            'parity': serial.PARITY_NONE,
            'stopbits': serial.STOPBITS_ONE,
            'bytesize': serial.EIGHTBITS,
            'timeout': 5,
            'port': self.configs['connection']['port']
        }

        self.logger.info('Connecting using parameters:\n%s', dumps(connection_params, indent=4))

        try:
            self.serial_port_obj = serial.Serial(**connection_params)
        except serial.serialutil.SerialException as exception:
            sys.exit(f'An exception occurred when connecting: "{exception}"')

        if not self.serial_port_obj.is_open:
            sys.exit(f'Could not connect to "{self.serial_port_obj.name}"')

        # Opening a connection will send a DTR (Data Terminal Ready) signal to device, which will
        # force the device to reset. Give device 2 seconds to reset

        self.logger.debug('DTR (Data Terminal Ready) was sent. Waiting for device to reset')
        sleep(2)

        return self

    def __exit__(self: T, *args) -> None:

        if self.serial_port_obj is None:
            self.logger.info('Not closing connection. Connection was never opened!')
            return

        self.logger.info('Closing connection!')

        if self.serial_port_obj.is_open:

            self.send_message('exit')
            self.receive_message()
            self.serial_port_obj.close()

    def send_message(self: T, message: str) -> None:

        self.logger.debug('Sending message: "%s"', message)
        message = message.encode(encoding=self.configs['connection']['encoding'])

        self.logger.debug('Sent %i bytes', self.serial_port_obj.write(message))
        self.serial_port_obj.flush()

    def receive_message(self: T) -> Tuple[bool, str]:

        self.logger.debug('Waiting to receive message...')
        message_received = False

        while not message_received:

            while self.serial_port_obj.in_waiting < 1:
                pass

            bytes_from_dev = self.serial_port_obj.read_until()  # Reads until \n by default
            message_received = True

        if len(bytes_from_dev) > 40:
            self.logger.debug('Received message: %s...', bytes_from_dev[:40])
            self.logger.debug('Message was truncated due to excessive length')
        else:
            self.logger.debug('Received message: %s', bytes_from_dev)

        try:
            results = bytes_from_dev.decode(self.configs['connection']['encoding']).strip()
        except UnicodeDecodeError as e:
            return False, f'An exception occurred when decoding results: "{e}"'

        status, message = results.split(';')

        return int(status) == 1, message
