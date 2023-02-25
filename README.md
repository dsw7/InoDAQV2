# InoDAQV2
A multifunction I/O device built atop the ATmega328P microprocessor.
## Table of Contents
- [Setup](#setup)
    - [Hardware requirements](#hardware-requirements)
    - [Python requirements](#python-requirements)
    - [Uploading code to device](#uploading-code-to-device)
    - [Testing device connectivity](#testing-device-connectivity)
- [Usage](#usage)
    - [Specifying a serial port](#specifying-a-serial-port)

## Setup

### Hardware requirements
While optional, it is strongly recommended to install [arduino-cli](https://github.com/arduino/arduino-cli).
This project's build system is based upon `arduino-cli`. To install `arduino-cli`, follow the
[Quickstart](https://github.com/arduino/arduino-cli#quickstart) section provided by the `arduino-cli`
developers. Alternatively, the `src/ino/ino.ino` "sketch" can be manually uploaded to the device via the
Arduino IDE.

If using `arduino-cli`, ensure that the Fully Qualified Board Name (FQBN) variable is updated in the
`Makefile`. This project was built atop an Uno which is reflected in the `Makefile`. If not working with an
Uno, change the FQBN as follows:
```
sed -i 's/FULLY_QUALIFIED_BOARD_NAME = arduino:avr:uno/FULLY_QUALIFIED_BOARD_NAME = <your-fqbn>/' Makefile
```
**NOTE:** This project was only tested with the Arduino Uno. Other boards may or may not be compatible.

### Python requirements
This project's GUI and API are written in Python and use several Python libraries. These libraries must be
installed. To install the libraries:
```
python3 -m pip install --user --requirement requirements.txt
```

### Uploading code to device
The code located in this repository must be uploaded to the device. To upload the code, run the `upload`
`make` target:
```
make upload SERIAL_PORT=<serial-port>
```
The `<serial-port>` argument can be either a COM port (if running from a Windows based host) or a device file
(if running from a Linux based host). In general, a serial port `COM<n>` maps to a device file `/dev/ttyS<n -
1>`. For example, `COM3` would map to `/dev/ttyS2`. This mapping may be relevant if running this program on
Cygwin.

### Testing device connectivity
Unit tests can be run against the device as a final sanity check. Ensure that the device is plugged into a
free serial port and run the following `make` target:
```
make test SERIAL_PORT=<serial-port>
```

## Usage
To use the product, run:
```
python3 src/py/main.py
```
If the unit tests under the [Testing device connectivity](#testing-device-connectivity) section passed, this
invocation should start a GUI. Additionally, the program should begin to log to the command line. If the
device is not plugged in, the command line will log an error indicating that the target serial port could not
be opened.

### Specifying a serial port
By default, this device attempts to connect to the serial port "COM3" (or `/dev/ttyS2`). A different serial
port can be specified via [inodaqv2.ini](./src/configs/inodaqv2.ini) - specifically the "port" field.
