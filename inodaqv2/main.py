import sys
from json import loads
from typing import Union
from flask import Flask, render_template, request, jsonify
from werkzeug.wrappers.response import Response
from click import command, option
from inoio import errors
from inodaqv2.components.extensions import conn

app = Flask(__name__)


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


@app.route("/", methods=["GET", "POST"])
def dashboard() -> Union[Response, str]:
    if request.is_json:
        if request.method == "POST":
            payload = loads(request.data)

            if payload["action"] == "dig":
                return jsonify(toggle_digital_pins(payload["pin"], payload["state"]))

    return render_template("dashboard.html")


@command()
@option("--host", default="localhost", help="Which host to bind to")
@option("--port", default=8045, help="Which TCP port to listen on")
@option(
    "--serial-port", default="/dev/ttyS2", help="Specify which USB device to connect to"
)
def main(host: str, port: int, serial_port: str) -> None:
    conn.init_app(port=serial_port)

    try:
        conn.connect()
    except errors.InoIOConnectionError as e:
        sys.exit(e)

    app.run(host=host, port=port)


if __name__ == "__main__":
    main()
