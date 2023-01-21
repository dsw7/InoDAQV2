from pytest import fixture
from src.py.serial_connection import SerialConnection

@fixture(scope='module')
def connection() -> SerialConnection:
    with SerialConnection() as conn:
        yield conn
