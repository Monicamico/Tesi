from flask import Flask
from plant import plant
import serial

# Mac
MICROBIT_PORT_MAC = '/dev/cu.usbmodem14202'


def write_serial(port):
    with serial.Serial(port, 115200) as s:
        s.write(b'.')
    s.close()


def create_app():
    app = Flask(__name__)
    app.register_blueprint(plant)
    return app


if __name__ == "__main__":
    #app = create_app()
    #app.run(port=5001)
    write_serial(MICROBIT_PORT_MAC)

