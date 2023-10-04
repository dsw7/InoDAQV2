import sys
from pathlib import Path
from tempfile import gettempdir
from subprocess import run, CalledProcessError
import click
import inodaqv2

PATH_SRC = Path(inodaqv2.__file__).parent
BUILD_DIR = Path(gettempdir()) / "inodaq-v2-build"
CACHE_DIR = Path(gettempdir()) / "inodaq-v2-core-cache"


def compile_source(port: str, fqbn: str) -> None:
    cmd = [
        "arduino-cli",
        "compile",
        "--verbose",
        f"--port={port}",
        f"--fqbn={fqbn}",
        f"--build-path={BUILD_DIR}",
        f"--build-cache-path={CACHE_DIR}",
        "ino",
    ]

    try:
        run(cmd, check=True, cwd=PATH_SRC)
    except CalledProcessError as e:
        sys.exit(f"Compilation failed with code {e.returncode}")


def upload_source(port: str, fqbn: str) -> None:
    cmd = [
        "arduino-cli",
        "upload",
        "--verbose",
        f"--port={port}",
        f"--fqbn={fqbn}",
        f"--input-dir={BUILD_DIR}",
        "ino",
    ]

    try:
        run(cmd, check=True, cwd=PATH_SRC)
    except CalledProcessError as e:
        sys.exit(f"Upload failed with code {e.returncode}")


@click.command()
@click.option("--serial-port", default="COM3", help="Specify serial port")
@click.option(
    "--fqbn", default="arduino:avr:uno", help="Specify fully qualified board name"
)
def main(serial_port: str, fqbn: str) -> None:
    compile_source(serial_port, fqbn)
    upload_source(serial_port, fqbn)


if __name__ == "__main__":
    main()
