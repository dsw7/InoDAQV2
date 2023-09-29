import sys
from pathlib import Path
from tempfile import gettempdir
from subprocess import run, CalledProcessError

FULLY_QUALIFIED_BOARD_NAME = "arduino:avr:uno"
BUILD_DIR = Path(gettempdir()) / "inodaq-v2-build"
CACHE_DIR = Path(gettempdir()) / "inodaq-v2-core-cache"


def compile_source(port: str) -> None:
    command = [
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
        run(command, check=True)
    except CalledProcessError as e:
        sys.exit(f"Compilation failed with code {e.returncode}")


def upload_source(port: str) -> None:
    command = [
        "arduino-cli",
        "upload",
        "--verbose",
        f"--port={port}",
        f"--fqbn={FULLY_QUALIFIED_BOARD_NAME}",
        f"--input-dir={BUILD_DIR}",
        "ino",
    ]

    try:
        run(command, check=True)
    except CalledProcessError as e:
        sys.exit(f"Upload failed with code {e.returncode}")


def main() -> None:
    try:
        port = sys.argv[1]
    except IndexError:
        sys.exit(f"Usage: $ python3 {sys.argv[0]} <port>")

    compile_source(port)
    upload_source(port)


if __name__ == "__main__":
    main()
