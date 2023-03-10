# InoDAQV2
A multifunction I/O device built atop the ATmega328P microprocessor.
## Table of Contents
- [Setup](#setup)
    - [Hardware requirements](#hardware-requirements)
    - [Python requirements](#python-requirements)
    - [Specifying a serial port](#specifying-a-serial-port)
    - [Uploading code to device](#uploading-code-to-device)
    - [Testing device connectivity](#testing-device-connectivity)
- [Usage](#usage)
    - [Window: Digital](#window-digital)
    - [Window: PWM](#window-pwm)
    - [Window: AnalogRead](#window-analogread)
    - [Window: DigitalRead](#window-digitalread)

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

### Specifying a serial port
Once the requirements have been installed, the serial port by which the device will transmit data must be
specified. The port can be specified by modifying the "port" field in
[inodaqv2.ini](./src/configs/inodaqv2.ini). On Windows this field would refer to a COM port (i.e. `COM3`) and
on Linux based systems this field would refer to the full path to a device file (i.e. `/dev/ttyS2`).

### Uploading code to device
The code located in this repository must be uploaded to the device. To upload the code, run the `upload`
`make` target:
```
make upload
```
**NOTE:** Cygwin is unique. A device file should be specified in [inodaqv2.ini](./src/configs/inodaqv2.ini)
but the equivalent COM port should be specified when running the `make` target:
```
make upload SERIAL_PORT=<com-port>
```
In general, a serial port `COM<n>` maps to a device file `/dev/ttyS<n - 1>`. For example, `COM3` would map to
`/dev/ttyS2`.

### Testing device connectivity
Unit tests can be run against the device as a final sanity check. Ensure that the device is plugged into a
free serial port and run the following `make` target:
```
make test
```
**NOTE:** Cygwin is unique. A device file should be specified in [inodaqv2.ini](./src/configs/inodaqv2.ini)
but the equivalent COM port should be specified when running the `make` target:
```
make upload SERIAL_PORT=<com-port>
```
In general, a serial port `COM<n>` maps to a device file `/dev/ttyS<n - 1>`. For example, `COM3` would map to
`/dev/ttyS2`.

## Usage
To use the product, run:
```
python3 src/py/main.py
```
If the unit tests under the [Testing device connectivity](#testing-device-connectivity) section passed, this
invocation should start a GUI. Additionally, the program should begin to log to the command line. If the
device is not plugged in, the command line will log an error indicating that the target serial port could not
be opened. The GUI is broken up into several "windows" - with each window serving a specific role. The
following sections describe the windows in more detail.

### Window: Digital
This window is used to toggle digital pins 2 through 13 on the device. The pins toggle to either a HIGH or LOW
state. Toggling pin 13 on an Uno device should turn the onboard LED either on or off. This behaviour can be
used as a sanity check.

### Window: PWM
This window can be used to emit a PWM wave on any PWM compatible digital pin. The slider is used to select the
duty cycle of the emitted wave. The PWM output frequency is approximately 490 Hz.

### Window: AnalogRead
This window can be used to read the analog voltages on analog pins A0 through A5.

### Window: DigitalRead
This window can be used to read the binary states of analog pins A0 through A5.
