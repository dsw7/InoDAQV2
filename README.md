# InoDAQV2
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A multifunction I/O device built atop the ATmega328P microprocessor.
## Table of Contents
- [Setup](#setup)
  - [Step 1 - Install `arduino-cli`](#step-1)
  - [Step 2 - Install package](#step-2---install-package)
  - [Step 3 - Upload source](#step-3---upload-source)
  - [Step 4 - Start webserver](#step-4---start-webserver)
- [Usage](#usage)
  - [Window: Digital](#window-digital)
  - [Window: PWM](#window-pwm)
  - [Window: AnalogRead](#window-analogread)
  - [Window: DigitalRead](#window-digitalread)

## Setup
### Step 1 - Install `arduino-cli`
This project uses [arduino-cli](https://github.com/arduino/arduino-cli) to upload Arduino source code to the
target device.  To install `arduino-cli`, follow the
[Quickstart](https://github.com/arduino/arduino-cli#quickstart) section provided by the `arduino-cli`
developers.

If using `arduino-cli`, ensure that the Fully Qualified Board Name (FQBN) variable is updated in the
`Makefile`. This project was built atop an Uno which is reflected in the `Makefile`. If not working with an
Uno, change the FQBN as follows:
```
sed -i 's/FULLY_QUALIFIED_BOARD_NAME = arduino:avr:uno/FULLY_QUALIFIED_BOARD_NAME = <your-fqbn>/' Makefile
```
**NOTE:** This project was only tested with the Arduino Uno. Other boards may or may not be compatible.
### Step 2 - Install package
To install the `inodaqv2` Python package, run:
```
make setup
```
The installation process will produce some build artifacts. These artifacts can be cleaned up by running:
```
make clean
```
### Step 3 - Upload source
The `inodaqv2` Python package includes utilities for uploading Arduino source code to the target device. To
upload the source, run:
```
inodaq-upload <serial-port>
```
Where `<serial-port>` would refer to a valid serial device, such as `COM3` on Windows or `/dev/ttyS2` on
Linux.
### Step 4 - Start webserver
As a final sanity check, run the webserver:
```
inodaq <serial-port>
```
This command will host a site locally using Flask's internal development server. Note that this webserver
should not be used in a production environment. A URL will be printed to the console if a connection to the
serial device is successfully established. Navigate to this URL to use the product.
## Usage
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
