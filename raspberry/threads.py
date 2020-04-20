import threading
import time
import requests as rq
import serial
from constants import URL_DASHBOARD, MICROBIT_PORT_MAC, Operation
from plant import requests

try:
    s = serial.Serial(MICROBIT_PORT_MAC, 115200)
    dummy = s.readline()
    print('Dummy byte received: ' + str(dummy))
except serial.serialutil.SerialException:
    print("\nNo such file or directory: "+MICROBIT_PORT_MAC)
    exit(1)


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
    line = byte.decode(encoding='UTF-8').strip()
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

        try:
            for request, serial_number, ping, param in read_serial():

                request = int(request)

                if request == Operation.CONNECTION.value:
                    print("connection request: " + serial_number)
                    reply = rq.put(url=URL_DASHBOARD + '/add_conn_request', json={'serial': serial_number, 'ping': ping})
                    print(reply)

                elif request == Operation.REFUSED.value:
                    print('refused: ' + serial_number)
                    reply = rq.put(url=URL_DASHBOARD + '/delete_conn_request',
                                   json={'serial': serial_number, 'ping': ping})
                    print(reply)

                elif request == Operation.JOINED.value:
                    print("joined: " + serial_number + ", " + ping)
                    reply = rq.put(url=URL_DASHBOARD + '/add_plant', json={'serial': serial_number, 'ping': ping})
                    print(reply)

                elif request == Operation.DELETED.value:
                    print("deleted: " + serial_number)
                    reply = rq.put(url=URL_DASHBOARD + '/delete_plant', json={'serial': serial_number})
                    print(reply)

                elif request == Operation.HUMIDITY.value:
                    print('humidity ' + serial_number + ': ' + param + ' ping: ' + ping)
                    reply = rq.put(url=URL_DASHBOARD + '/update_hum',
                                   json={'serial': serial_number, 'ping': ping, 'hum': param})
                    print(reply)

                elif request == Operation.TEMPERATURE.value:
                    print("temperature " + serial_number + ': ' + param + "\nping: " + ping)
                    reply = rq.put(url=URL_DASHBOARD + '/update_temp',
                                   json={'serial': serial_number, 'ping': ping, 'temp': param})
                    print(reply)

                elif request == Operation.LIGHT.value:
                    print("light " + serial_number + ': ' + param + "\nping: " + ping)
                    reply = rq.put(url=URL_DASHBOARD + '/update_light',
                                   json={'serial': serial_number, 'ping': ping, 'light': param})
                    print(reply)

                elif request == Operation.PING.value:
                    print("ping " + serial_number + ': ' + ping)
                    reply = rq.put(url=URL_DASHBOARD + '/update_ping', json={'serial': serial_number, 'ping': ping})
                    print(reply)

        except ValueError:
            pass


def writer():
    while True:
        w = 0
        while len(requests) != 0 and w != 5:
            st = requests.pop()
            write_serial(st)
            w = w + 1
        time.sleep(20)
