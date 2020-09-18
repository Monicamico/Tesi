import threading
import time
import serial
import requests as rq
from constants import URL_DASHBOARD, PORT, MICROBIT_PORT_MAC, MICROBIT_PORT_MAC2, MICROBIT_PORT_LINUX2
from request import request_queue
from utility import get_ip, lock_queue, condition_variable
from constants import MICROBIT_PORT_LINUX, Operation, DELIMITER


global s
try:
    s = serial.Serial(MICROBIT_PORT_MAC2, 115200)
    print(MICROBIT_PORT_MAC2 + ' opened...')
except serial.serialutil.SerialException:
    print("\nNo such file or directory: " + MICROBIT_PORT_MAC2)

    try:
        s = serial.Serial(MICROBIT_PORT_MAC, 115200)
        print(MICROBIT_PORT_MAC + ' opened...')
    except serial.serialutil.SerialException:
        print("\nNo such file or directory: " + MICROBIT_PORT_MAC)

        try:
            s = serial.Serial(MICROBIT_PORT_LINUX, 115200)
            print(MICROBIT_PORT_LINUX + ' opened...')
        except serial.serialutil.SerialException:
            print("\nNo such file or directory: " + MICROBIT_PORT_LINUX)

            try:
                s = serial.Serial(MICROBIT_PORT_LINUX2, 115200)
                print(MICROBIT_PORT_LINUX2 + ' opened...')
            except serial.serialutil.SerialException:
                print("\nNo such file or directory: " + MICROBIT_PORT_LINUX2)


"""
s.timeout = 1
dummy = s.readline()
s.timeout = None
print('Dummy byte received: ' + str(dummy))
"""
ip_address = get_ip()
URL = str(ip_address) + ":" + str(PORT)
print(URL)


class Reader(threading.Thread):
    """
    Thread Reader
    """
    def __init__(self, nome):
        threading.Thread.__init__(self)
        self.nome = nome

    def run(self):
        """

        Method representing the thread’s activity.

        It calls the function *reader()*
        """
        print(self.nome + " started!")
        reader()


class Writer(threading.Thread):
    """
    Thread Writer
    """
    def __init__(self, nome):
        threading.Thread.__init__(self)
        self.nome = nome

    def run(self):
        """
        Method representing the thread’s activity.

        It calls the function *writer()*

        """
        print(self.nome + " started!")
        writer()


def read_serial():
    """

    Read a row from the serial port.

    :return: request, serial number, signal, param
    :rtype: str
    """
    byte = s.readline()
    line = byte.decode(encoding='UTF-8').strip()
    try:
        req, s_n, signal_, param_ = line.split(";")
        yield req, s_n, signal_, param_
    except ValueError:
        pass


def write_serial(data):
    """
    Writes data in the serial port.

    :param data: data to be written in the serial port
    :type data: str
    :return: len(data)
    :rtype: int

    """
    content = bytes(data, 'utf-8')
    try:
        return s.write(content)
    except ValueError as err:
        print(err)


# Request or response from RADIO-dashboard
def reader():
    """
    Called from the Thread Reader, to read request/response from radio-microbit.
    if the request/response received is valid send it to the dashboard,
    trow HTTP request.
    """
    while True:
        for request, serial_number, signal, param in read_serial():
            print("Response from Radio:")

            if request is not None:
                request = int(request)
                valid_request = False
                for op in Operation:
                    if op.value == request:
                        valid_request = True
            else:
                continue

            if param is not None:
                valid_request_param = True
            else:
                valid_request_param = False

            if request == Operation.SET_TEMPERATURE_MAX.value or request == Operation.SET_TEMPERATURE_MIN.value or request == Operation.TEMPERATURE.value:
                param = int(param)
                if valid_request_param and param >= 0:
                    valid_request = True
                else:
                    valid_request = False

            if request == Operation.SET_HUMIDITY_MIN.value or request == Operation.SET_HUMIDITY_MAX.value or request == Operation.HUMIDITY:
                if valid_request_param and 0 <= int(param) <= 1023:
                    param = int(param)
                    valid_request = True
                else:
                    valid_request = False

            if request == Operation.SET_LIGHT_MIN.value or request == Operation.SET_LIGHT_MAX.value \
                    or request == Operation.SET_WATERING_LIGHT.value or request == Operation.LIGHT:
                param = int(param)
                if valid_request_param and 0 <= param <= 255:
                    valid_request = True
                else:
                    valid_request = False

            if request == Operation.SET_WATER_CONTAINER_SIZE.value:
                param = float(param)
                if valid_request_param and param > 0:
                    valid_request = True
                else:
                    valid_request = False

            if request == Operation.WATER_CONTAINER_STATE.value:
                param = int(param)
                if valid_request_param and (param == 1 or param == 0):
                    valid_request = True
                else:
                    valid_request = False

            if request == Operation.VASE_TRANSMIT_POWER.value:
                param = int(param)
                if valid_request_param:
                    valid_request = True
                else:
                    valid_request = False

            if request == Operation.RADIO_TRANSMIT_POWER.value:
                param = int(param)
                if valid_request_param:
                    valid_request = True
                else:
                    valid_request = False

            if request == Operation.SET_RADIO_PAUSE_TIME.value:
                param = int(param)
                if valid_request_param and param > 0.0:
                    valid_request = True
                else:
                    valid_request = False

            if request == Operation.SET_VASE_SEND_TIME.value:
                param = int(param)
                if valid_request_param and param > 0:
                    valid_request = True
                else:
                    valid_request = False

            if request == Operation.RADIO_JOIN.value:
                lock_queue.acquire()
                to_send = str(Operation.RADIO_JOIN.value) + DELIMITER
                request_queue.append(to_send)
                condition_variable.notify_all()
                lock_queue.release()

            if request == Operation.DELETED.value:
                valid_request = True

            if request == Operation.REFUSED.value:
                valid_request = True

            if valid_request:
                if serial_number is not None:
                    if param is not None:
                        print(str(request)+" / " + serial_number + "/ " + str(param))
                        if request == Operation.CONNECTION.value:
                            reply = rq.put(url=URL_DASHBOARD + '/request',
                                           json={'request': request,
                                                 'signal': signal,
                                                 'serial': serial_number,
                                                 'url': URL,
                                                 'param': param})
                        else:
                            reply = rq.put(url=URL_DASHBOARD + '/request',
                                           json={'request': request,
                                                 'serial': serial_number,
                                                 'url': URL,
                                                 'param': param})
                    else:
                        print(str(request) + " / " + serial_number)
                        reply = rq.put(url=URL_DASHBOARD + '/request',
                                       json={'request': request,
                                             'serial': serial_number,
                                             'url': URL})
                    print(reply)

                else:
                    print("No serial number received.")
            else:
                print("No valid request received.")


def writer():
    """
    Called from the Thread Writer, to take the requests from the queue (dashboard's requests)
    and to send them to the microbit, writing the data of the requests into the serial port.
    """
    while True:
        lock_queue.acquire()
        while len(request_queue) == 0:
            condition_variable.wait()
        st = request_queue.pop()
        if write_serial(st) <= 0:
            raise Exception
        lock_queue.release()
        print("Thread Writer, Scritto su radio: " + st)
        time.sleep(3)


