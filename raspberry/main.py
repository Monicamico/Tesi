import serial
from flask import Flask
from plant import plant
from threads import Reader, Writer
from costants import MICROBIT_PORT_MAC


def create_app():
    app = Flask(__name__)
    app.register_blueprint(plant)
    return app


if __name__ == "__main__":

    try:
        with serial.Serial(MICROBIT_PORT_MAC, 115200) as s:
            print("port opened...")
    except serial.serialutil.SerialException:
        print("\n Porta seriale non trovata")
        exit(2)

    try:
        thread_reader = Reader("Thread Reader", s)
        thread_writer = Writer("Thread Writer", s)
        thread_reader.start()
        thread_writer.start()
    except NameError:
        print("Parametro s inesistente\n")
        exit(1)

    app = create_app()
    app.run(port=5001)