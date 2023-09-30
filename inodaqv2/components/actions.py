from inoio import errors
from inodaqv2.components.extensions import conn


def toggle_digital_pins(pin: str, state: bool) -> dict[str, str]:
    pin_id = pin.split("-")[1]

    command = f"dig:{pin_id}:"

    if state:
        command += "on"
    else:
        command += "off"

    try:
        conn.write(command)
    except errors.InoIOTransmissionError as e:
        message = str(e)
    else:
        message = conn.read()

    return {"command": command, "message": message}


def read_analog_pins() -> dict[str, int]:
    try:
        conn.write("aread")
    except errors.InoIOTransmissionError as e:
        message = str(e)
    else:
        message = conn.read()

    _, values = message.split(";")
    analog_to_volt = 5.0 / 1023

    payload = {}
    for u, v in enumerate(values.split(",")):
        payload[f"A{u}"] = round(int(v) * analog_to_volt, 3)

    return payload
