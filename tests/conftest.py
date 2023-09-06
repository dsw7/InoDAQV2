from pathlib import Path
from configparser import ConfigParser
from typing import Generator
from pytest import fixture
from inodaqv2.serial_connection import SerialConnection


@fixture(scope="session")
def connection() -> Generator[SerialConnection, None, None]:
    path_ini = Path(__file__).parents[1] / "configs/inodaqv2.ini"

    configs = ConfigParser()
    configs.read(path_ini)

    with SerialConnection(configs["connection"]) as conn:
        yield conn
