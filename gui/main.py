import sys
from json import loads
from typing import Union
from flask import Flask, render_template, request, jsonify
from werkzeug.wrappers.response import Response
from click import command, option
from inoio import errors
from gui import actions
from gui.extensions import conn
from gui.logger import setup_logger

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def dashboard() -> Union[Response, str]:
    if request.is_json:
        if request.method == "POST":
            payload = loads(request.data)

            if payload["action"] == "dig":
                return jsonify(
                    actions.toggle_digital_pins(payload["pin"], payload["state"])
                )

            if payload["action"] == "aread":
                return jsonify(actions.read_analog_pins())

            if payload["action"] == "dread":
                return jsonify(actions.read_digital_pins())

            if payload["action"] == "pwm":
                return jsonify(actions.set_pwm(payload["pin"], payload["value"]))

            if payload["action"] == "tone":
                return jsonify(actions.set_tone(payload["pin"], payload["frequency"]))

    return render_template("dashboard.html")


@command()
@option("--host", default="localhost", help="Which host to bind to")
@option("--port", default=8045, help="Which TCP port to listen on")
@option(
    "--serial-port", default="/dev/ttyS2", help="Specify which USB device to connect to"
)
def main(host: str, port: int, serial_port: str) -> None:
    setup_logger()
    conn.init_app(port=serial_port)

    try:
        conn.connect()
    except errors.InoIOConnectionError as e:
        sys.exit(e)

    try:
        actions.run_handshake()
    except ConnectionError as e:
        sys.exit(str(e))

    app.run(host=host, port=port)


if __name__ == "__main__":
    main()
