import serial, requests as rq

URL = 'http://127.0.0.1:5000'
# Linux
MICROBIT_PORT_LINUX = '/dev/ttyACM0'

# Mac
MICROBIT_PORT_MAC = '/dev/cu.usbmodem14202'


def read_serial(port):
    with serial.Serial(port, 115200) as s:
        print("reading serial port...")
        while True:
            byte = s.readline()
            line = byte.decode().strip()
            try:
                req, s_n, ping_, param_ = line.split(";")
                yield req, s_n, ping_, param_
            except ValueError as err:
                print(err)


if __name__ == "__main__":
    header = {'Content-type': 'application/json'}
    for request, serial_number, ping, param in read_serial(MICROBIT_PORT_MAC):

        print(request + " " + serial_number)

        if "conn_req" in request:
            reply = rq.put(url=URL + '/add_conn_request', json={'serial': serial_number, 'ping': ping})
            print(reply)

        elif "refused" in request:
            reply = rq.put(url=URL + '/delete_conn_request',
                           json={'serial': serial_number, 'ping': ping})
            print(reply)

        elif "joined" in request:
            print("ping: " + ping)
            reply = rq.put(url=URL + '/add_plant', json={'serial': serial_number, 'ping': ping})
            print(reply)

        elif "deleted" in request:
            reply = rq.put(url=URL + '/delete_plant', json={'serial': serial_number})
            print(reply)

        elif "getHum" in request:
            print("value: " + param + " ping: " + ping)
            reply = rq.put(url=URL + '/update_hum', json={'serial': serial_number, 'ping': ping, 'hum': param})
            print(reply)

        elif "getTemp" in request:
            print("value: " + param + " ping: " + ping)
            reply = rq.put(url=URL + '/update_temp', json={'serial': serial_number, 'ping': ping, 'temp': param})
            print(reply)

        elif "getLight" in request:
            print("value: " + param + " ping: " + ping)
            reply = rq.put(url=URL + '/update_light', json={'serial': serial_number, 'ping': ping, 'light': param})
            print(reply)

        elif "ping" in request:
            print(param)
            reply = rq.put(url=URL + '/update_ping', json={'serial': serial_number, 'ping': ping})
            print(reply)
