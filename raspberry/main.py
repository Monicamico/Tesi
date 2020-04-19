import time, serial, threading
import requests as rq
from flask import Flask
from plant import plant, requests

URL_RASPBERRY = 'http://127.0.0.1:5001'
URL_DASHBOARD = 'http://127.0.0.1:5000'

# Linux
MICROBIT_PORT_LINUX = '/dev/ttyACM0'
# Mac
MICROBIT_PORT_MAC = '/dev/cu.usbmodem14202'


class Reader(threading.Thread):
    def __init__(self, nome):
        threading.Thread.__init__(self)
        self.nome = nome

    def run(self):
        print(self.nome + "started!")
        reader()


class Writer(threading.Thread):
    def __init__(self, nome):
        threading.Thread.__init__(self)
        self.nome = nome

    def run(self):
        print(self.nome + "started!")
        writer()


def read_serial():
    byte = s.readline()
    line = byte.decode().strip()
    try:
        req, s_n, ping_, param_ = line.split(";")
        return req, s_n, ping_, param_
    except ValueError as err:
        print(err)


def write_serial(data):
    content = bytes(data, 'utf-8')
    try:
        s.write(content)
    except ValueError as err:
        print(err)


def reader():
    while True:
        for request, serial_number, ping, param in read_serial(MICROBIT_PORT_MAC):

            print(request + " " + serial_number)

            if "conn_req" in request:
                reply = rq.put(url=URL_DASHBOARD + '/add_conn_request', json={'serial': serial_number, 'ping': ping})
                print(reply)

            elif "refused" in request:
                reply = rq.put(url=URL_DASHBOARD + '/delete_conn_request',
                               json={'serial': serial_number, 'ping': ping})
                print(reply)

            elif "joined" in request:
                print("ping: " + ping)
                reply = rq.put(url=URL_DASHBOARD + '/add_plant', json={'serial': serial_number, 'ping': ping})
                print(reply)

            elif "deleted" in request:
                reply = rq.put(url=URL_DASHBOARD + '/delete_plant', json={'serial': serial_number})
                print(reply)

            elif "getHum" in request:
                print("value: " + param + " ping: " + ping)
                reply = rq.put(url=URL_DASHBOARD + '/update_hum', json={'serial': serial_number, 'ping': ping, 'hum': param})
                print(reply)

            elif "getTemp" in request:
                print("value: " + param + " ping: " + ping)
                reply = rq.put(url=URL_DASHBOARD + '/update_temp', json={'serial': serial_number, 'ping': ping, 'temp': param})
                print(reply)

            elif "getLight" in request:
                print("value: " + param + " ping: " + ping)
                reply = rq.put(url=URL_DASHBOARD + '/update_light', json={'serial': serial_number, 'ping': ping, 'light': param})
                print(reply)

            elif "ping" in request:
                print(param)
                reply = rq.put(url=URL_DASHBOARD + '/update_ping', json={'serial': serial_number, 'ping': ping})
                print(reply)


def writer():
    while True:
        w = 0
        while requests.count() != 0 | w != 5:
            st = requests.pop()
            write_serial(st)
        time.sleep(20)


def create_app():
    app = Flask(__name__)
    app.register_blueprint(plant)
    return app


if __name__ == "__main__":
    with serial.Serial(MICROBIT_PORT_MAC, 115200) as s:
        print("port opened...")

    thread_reader = Reader("Thread Reader")
    thread_writer = Writer("Thread Writer")

    thread_reader.start()
    thread_writer.start()

    thread_writer.join()
    thread_reader.join()

    app = create_app()
    app.run(port=5001)
