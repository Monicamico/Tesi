import threading
import time
import requests as rq
import serial
from costants import URL_DASHBOARD, MICROBIT_PORT_MAC
from plant import requests

s = serial.Serial(MICROBIT_PORT_MAC, 115200)


class Reader(threading.Thread):
    def __init__(self, nome):
        threading.Thread.__init__(self)
        self.nome = nome

    def run(self):
        print(self.nome + " started!")
        reader()


class Writer(threading.Thread):
    def __init__(self, nome):
        threading.Thread.__init__(self)
        self.nome = nome

    def run(self):
        print(self.nome + " started!")
        writer()


def read_serial():
    byte = s.readline()
    line = byte.decode().strip()
    try:
        req, s_n, ping_, param_ = line.split(";")
        yield req, s_n, ping_, param_
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
        for request, serial_number, ping, param in read_serial():

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
        while len(requests) != 0 and w != 5:
            st = requests.pop()
            write_serial(st)
            w = w + 1
        time.sleep(20)
