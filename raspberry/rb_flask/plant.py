from flask import Blueprint, render_template, request as http_req, redirect
import serial

MAC_RASPBERRY_PORT = '/dev/tty.usbmodem14202'


def write_serial(port, data):

    with serial.Serial(port, 115200) as s:
        content = bytes(data, 'utf-8')
        s.write(content)


plant = Blueprint('plant', __name__)


@plant.route("/water", methods=['POST', 'PUT'])
def water():
    data = http_req.json
    s = str(data)
    s_list = s.split(":")
    s_list = s_list[1].split("'")
    to_send = "water;"+s_list[1]
    print(to_send)
    write_serial(MAC_RASPBERRY_PORT, to_send)
    return redirect("http://127.0.0.1:5000/plant/" + data['serial'])

