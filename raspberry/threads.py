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
        # request from radio
        for request, serial_number, ping, param in read_serial():

            if request is not None:
                request = int(request)
                valid_request = False
                for op in Operation:
                    if op.value == request:
                        valid_request = True
            else:
                continue

            if param is not None:
                param = int(param)
                valid_request_param = True
            else:
                valid_request_param = False

            if request == Operation.SET_TEMPERATURE_MAX.value or request == Operation.SET_TEMPERATURE_MIN.value or request == Operation.TEMPERATURE.value:
                if valid_request_param and param >= 0:
                    valid_request = True
                else:
                    valid_request = False

            if request == Operation.SET_HUMIDITY_MIN.value or request == Operation.SET_HUMIDITY_MAX.value or request == Operation.HUMIDITY:
                if valid_request_param and 0 <= param <= 1023:
                    valid_request = True
                else:
                    valid_request = False

            if request == Operation.SET_LIGHT_MIN.value or request == Operation.SET_LIGHT_MAX.value \
                    or request == Operation.SET_WATERING_LIGHT.value or request == Operation.LIGHT:
                if valid_request_param and 0 <= param <= 255:
                    valid_request = True
                else:
                    valid_request = False

            if request == Operation.SET_WATER_CONTAINER_SIZE.value:
                if valid_request_param and param > 0:
                    valid_request = True
                else:
                    valid_request = False

            if request == Operation.WATER_CONTAINER_STATE.value or request == Operation.VASE_STATE.value:
                if valid_request_param and (param == WaterContainerState.Empty or param == WaterContainerState.Full):
                    valid_request = True
                else:
                    valid_request = False

            if request == Operation.VASE_TRANSMIT_POWER.value or request == Operation.RADIO_TRANSMIT_POWER.value:
                if valid_request_param and (1 <= param <= 7):
                    valid_request = True
                else:
                    valid_request = False

            if request == Operation.RADIO_JOIN.value:
                to_send = str(Operation.RADIO_JOIN.value) + DELIMITER
                request_queue.append(to_send)

            if valid_request:
                if serial_number is not None:
                    if param:
                        print(str(request)+" / " + serial_number + ": " + str(param))
                        reply = rq.put(url=URL_DASHBOARD + '/request',
                                       json={'request': request,
                                             'serial': serial_number,
                                             'url': URL,
                                             'ping': ping,
                                             'param': param})
                    else:
                        print(str(request) + " / " + serial_number)
                        reply = rq.put(url=URL_DASHBOARD + '/request',
                                       json={'request': request,
                                             'serial': serial_number,
                                             'url': URL,
                                             'ping': ping})
                    print(reply)

                else:
                    print("No serial number received.")
            else:
                print("No valid request received.")


def writer():
    while True:
        w = 0
        while len(request_queue) != 0 and w != 5:
            st = request_queue.pop()
            write_serial(st)
            w = w + 1
