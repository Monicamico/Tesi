import threading
import time
import serial
import requests as rq
from constants import URL_DASHBOARD, PORT, WaterContainerState, VaseState
from request import request_queue
from utility import get_ip
from constants import MICROBIT_PORT_MAC, MICROBIT_PORT_MAC2, Operation, DELIMITER


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
        #exit(1)


ip_address = get_ip()
URL = 'http://' + str(ip_address) + ':' + str(PORT)
print(URL)


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

            if param is not None:
                param = int(param)

            if serial_number is not None:

                if request == Operation.RADIO_JOIN.value:
                    print("radio connection request: " + serial_number)
                    reply = rq.put(url=URL_DASHBOARD + '/radio_conn_request',
                                   json={'serial': serial_number,
                                         'url': URL})
                    tosend = str(Operation.RADIO_JOIN.value) + DELIMITER
                    request_queue.append(tosend)
                    print(reply)

                elif request == Operation.CONNECTION.value:
                    print("connection request: " + serial_number)
                    reply = rq.put(url=URL_DASHBOARD + '/add_conn_request',
                                   json={'serial': serial_number,
                                         'ping': ping,
                                         'pairing': param,
                                         'url': URL})
                    print(reply)

                elif request == Operation.REFUSED.value:
                    print('refused: ' + serial_number)
                    reply = rq.put(url=URL_DASHBOARD + '/delete_conn_request',
                                   json={'serial': serial_number, 'ping': ping, 'url': URL})
                    print(reply)

                elif request == Operation.JOINED.value:
                    print("joined: " + serial_number + ", " + ping)
                    reply = rq.put(url=URL_DASHBOARD + '/add_plant',
                                   json={'serial': serial_number,
                                         'ping': ping,
                                         'radio_serial': param,
                                         'url': URL})
                    print(reply)

                elif request == Operation.DELETED.value:
                    print("deleted: " + serial_number)
                    reply = rq.put(url=URL_DASHBOARD + '/delete_plant',
                                   json={'serial': serial_number, 'url': URL})
                    print(reply)

                elif request == Operation.HUMIDITY.value:
                    if 0 <= param <= 1023:
                        print('humidity ' + serial_number + ': ' + str(param) + " ping: " + ping)
                        reply = rq.put(url=URL_DASHBOARD + '/update_hum',
                                       json={'serial': serial_number,
                                             'ping': ping,
                                             'hum': param})
                        print(reply)

                elif request == Operation.TEMPERATURE.value:
                    print("temperature " + serial_number + ': ' + str(param) + 'ping: ' + ping)
                    reply = rq.put(url=URL_DASHBOARD + '/update_temp',
                                   json={'serial': serial_number,
                                         'ping': ping,
                                         'temp': param})
                    print(reply)

                elif request == Operation.LIGHT.value:
                    if 0 <= param <= 255:
                        print("light " + serial_number + ': ' + str(param) + 'ping: ' + ping)
                        reply = rq.put(url=URL_DASHBOARD + '/update_light',
                                       json={'serial': serial_number,
                                             'ping': ping,
                                             'light': param})
                        print(reply)

                elif request == Operation.PING.value:
                    print("ping " + serial_number + ': ' + ping)
                    reply = rq.put(url=URL_DASHBOARD + '/update_ping',
                                   json={'serial': serial_number,
                                         'ping': ping})
                    print(reply)

                elif request == Operation.WATER_CONTAINER_STATE.value:
                    if param is not None and (param == WaterContainerState.Full or WaterContainerState.Empty):
                        print("water container state " + serial_number + ': ' + str(param))
                        reply = rq.put(url=URL_DASHBOARD + '/update_water_container_state',
                                       json={'serial': serial_number,
                                             'ping': ping,
                                             'state': param})
                        print(reply)
                    else:
                        print("water container state " + serial_number + ": errore parametro")

                elif request == Operation.VASE_STATE.value:
                    if param is not None:
                        if param == 0 or 1:
                            print("vase state " + serial_number + ': ' + str(param))
                            reply = rq.put(url=URL_DASHBOARD + '/update_vase_state', json={'serial': serial_number,
                                                                                            'ping': ping,
                                                                                            'state': param})
                            print(reply)
                    else:
                        print("vase state " + serial_number + ": errore parametro")

                elif request == Operation.SET_LIGHT_MIN.value:
                    if param is not None and (0 <= param <= 255):
                        print("set light min " + serial_number + ': ' + str(param))
                        reply = rq.put(url=URL_DASHBOARD + '/update_light_min',
                                       json={'serial': serial_number,
                                             'ping': ping,
                                             'param': param})
                        print(reply)
                    else:
                        print("set light min " + serial_number + ": errore parametro")

                elif request == Operation.SET_LIGHT_MAX.value:
                    if param is not None and (0 <= param <= 255):
                        print("set light max " + serial_number + ': ' +str(param))
                        reply = rq.put(url=URL_DASHBOARD + '/update_light_max',
                                       json={'serial': serial_number,
                                             'ping': ping,
                                             'param': param})
                        print(reply)
                    else:
                        print("set light max " + serial_number + ": errore parametro")

                elif request == Operation.SET_WATERING_LIGHT.value:
                    if param is not None and (0 <= param <= 255):
                        print("set watering light " + serial_number + ': ' +str(param))
                        reply = rq.put(url=URL_DASHBOARD + '/update_watering_light',
                                       json={'serial': serial_number,
                                             'ping': ping,
                                             'param': param})
                        print(reply)
                    else:
                        print("set light max " + serial_number + ": errore parametro")

                elif request == Operation.SET_HUMIDITY_MIN.value:
                    if param is not None and (0 <= param <= 1023):
                        print("set humidity min " + serial_number + ': ' + str(param))
                        reply = rq.put(url=URL_DASHBOARD + '/update_hum_min',
                                       json={'serial': serial_number,
                                             'ping': ping,
                                             'param': param})
                        print(reply)
                    else:
                        print("set hum min " + serial_number + ": errore parametro")

                elif request == Operation.SET_HUMIDITY_MAX.value:
                    if param is not None and (0 <= param <= 1023):
                        print("set humidity max " + serial_number + ': ' + str(param))
                        reply = rq.put(url=URL_DASHBOARD + '/update_hum_max',
                                       json={'serial': serial_number,
                                             'ping': ping,
                                             'param': param})
                        print(reply)
                    else:
                        print("set hum max " + serial_number + ": errore parametro")

                elif request == Operation.SET_TEMPERATURE_MIN.value:
                    if param is not None and (0 <= param):
                        print("set temp min " + serial_number + ': ' + str(param))
                        reply = rq.put(url=URL_DASHBOARD + '/update_temp_min',
                                       json={'serial': serial_number,
                                             'ping': ping,
                                             'param': param})
                        print(reply)
                    else:
                        print('set temp min ' + serial_number + ": errore parametro")

                elif request == Operation.SET_TEMPERATURE_MAX.value:
                    if param is not None and (0 <= param):
                        print("set temp max " + serial_number + ': ' + str(param))
                        reply = rq.put(url=URL_DASHBOARD + '/update_temp_max',
                                       json={'serial': serial_number,
                                             'ping': ping,
                                             'param': param})
                        print(reply)
                    else:
                        print('set temp max ' + serial_number + ": errore parametro")

            else:
                print("No serial number received.")


def writer():
    while True:
        w = 0
        while len(request_queue) != 0 and w != 5:
            st = request_queue.pop()
            write_serial(st)
            w = w + 1
