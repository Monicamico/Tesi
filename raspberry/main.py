from constants import PORT
from utility import get_ip
from threads import Reader, Writer
from flask import Flask
from request import request_page


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
    except:
        print("ERRORE THREADS\n")
        exit(1)
    app = create_app()
    IP = get_ip()
    app.run(host=IP, port=PORT)
