from typing import Generator
from inoio import InoIO
from pytest import fixture


def pytest_addoption(parser):
    parser.addoption("--port", action="store", default="/dev/ttyS2")


@fixture(scope="session")
def connection(pytestconfig) -> Generator[InoIO, None, None]:
    port = pytestconfig.getoption("port")

    conn = InoIO(port=port)
    conn.connect()

    yield conn
    conn.disconnect()
