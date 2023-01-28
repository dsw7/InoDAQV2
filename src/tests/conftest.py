from pathlib import Path
from configparser import ConfigParser
from pytest import fixture
from src.py.serial_connection import SerialConnection

@fixture(scope='session')
def connection() -> SerialConnection:
    path_ini = Path(__file__).parents[1] / 'configs/inodaqv2.ini'

    configs = ConfigParser()
    configs.read(path_ini)

    with SerialConnection(configs['connection']) as conn:
        yield conn
