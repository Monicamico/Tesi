import threading
import time
import requests as rq
import serial
from constants import URL_DASHBOARD, MICROBIT_PORT_MAC, Operation, MICROBIT_PORT_MAC2
from request import request_queue

try:
    s = serial.Serial(MICROBIT_PORT_MAC, 115200)
    print(MICROBIT_PORT_MAC + ' opened...')
    s.timeout = 1
    dummy = s.readline()
    s.timeout = None
    print('Dummy byte received: ' + str(dummy))

except serial.serialutil.SerialException:
    print("\nNo such file or directory: " + MICROBIT_PORT_MAC)
    try:
        s = serial.Serial(MICROBIT_PORT_MAC2, 115200)
        print(MICROBIT_PORT_MAC2 + ' opened...')
        s.timeout = 1
        dummy = s.readline()
        s.timeout = None
        print('Dummy byte received: ' + str(dummy))
    except serial.serialutil.SerialException:
        print("\nNo such file or directory: " + MICROBIT_PORT_MAC2)
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
    except ValueError:
        pass


def write_serial(data):
    content = bytes(data, 'utf-8')
    try:
        s.write(content)
    except ValueError as err:
        print(err)


def reader():
    while True:
        for request, serial_number, ping, param in read_serial():

            if request is not None:
                request = int(request)
            else:
                continue

            if serial_number is not None:

                if request == Operation.CONNECTION.value:
                    print("connection request: " + serial_number)
                    reply = rq.put(url=URL_DASHBOARD + '/add_conn_request', json={'serial': serial_number,
                                                                                  'ping': ping,
                                                                                  'pairing': param})
                    print(reply)

                elif request == Operation.REFUSED.value:
                    print('refused: ' + serial_number)
                    reply = rq.put(url=URL_DASHBOARD + '/delete_conn_request',
                                   json={'serial': serial_number, 'ping': ping})
                    print(reply)

                elif request == Operation.JOINED.value:
                    print("joined: " + serial_number + ", " + ping)
                    reply = rq.put(url=URL_DASHBOARD + '/add_plant', json={'serial': serial_number,
                                                                           'ping': ping,
                                                                           'radio_serial': param })
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

                elif request == Operation.WATER_CONTAINER_STATE.value:
                    print("water container state " + serial_number + ': ' + param)
                    reply = rq.put(url=URL_DASHBOARD + '/update_water_container_state',
                                   json={'serial': serial_number, 'ping': ping, 'state': param})
                    print(reply)

                else:
                    pass
            else:
                print("No serial number received.")


def writer():
    while True:
        w = 0
        while len(request_queue) != 0 and w != 5:
            st = request_queue.pop()
            write_serial(st)
            w = w + 1
            time.sleep(2)
