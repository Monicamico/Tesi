import serial
from flask import Flask
from request import request_page
from threads import Reader, Writer


def create_app():
    app = Flask(__name__)
    app.register_blueprint(request_page)
    return app


if __name__ == "__main__":

    try:
        thread_reader = Reader("Thread Reader")
        thread_writer = Writer("Thread Writer")
        thread_reader.start()
        thread_writer.start()
    except NameError:
        print("Parametro s inesistente\n")
        exit(1)

    app = create_app()
    app.run(port=5001)