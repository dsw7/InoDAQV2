import sys
from pathlib import Path
from tempfile import gettempdir
from subprocess import run, CalledProcessError
from click import command, argument
import inodaqv2

PATH_SRC = Path(inodaqv2.__file__).parent
FULLY_QUALIFIED_BOARD_NAME = "arduino:avr:uno"
BUILD_DIR = Path(gettempdir()) / "inodaq-v2-build"
CACHE_DIR = Path(gettempdir()) / "inodaq-v2-core-cache"


def compile_source(port: str) -> None:
    cmd = [
        "arduino-cli",
        "compile",
        "--verbose",
        f"--port={port}",
        f"--fqbn={FULLY_QUALIFIED_BOARD_NAME}",
        f"--build-path={BUILD_DIR}",
        f"--build-cache-path={CACHE_DIR}",
        "ino",
    ]

    try:
        run(cmd, check=True, cwd=PATH_SRC)
    except CalledProcessError as e:
        sys.exit(f"Compilation failed with code {e.returncode}")


def upload_source(port: str) -> None:
    cmd = [
        "arduino-cli",
        "upload",
        "--verbose",
        f"--port={port}",
        f"--fqbn={FULLY_QUALIFIED_BOARD_NAME}",
        f"--input-dir={BUILD_DIR}",
        "ino",
    ]

    try:
        run(cmd, check=True, cwd=PATH_SRC)
    except CalledProcessError as e:
        sys.exit(f"Upload failed with code {e.returncode}")


@command()
@argument("serial-port", default="COM3")
def main(serial_port: str) -> None:
    compile_source(serial_port)
    upload_source(serial_port)


if __name__ == "__main__":
    main()
