from flask import Blueprint, render_template, request as http_req, redirect
import serial

URL_RASPBERRY = 'http://127.0.0.1:5001'
URL_DASHBOARD = 'http://127.0.0.1:5000'
MICROBIT_PORT_MAC = '/dev/cu.usbmodem14202'

plant = Blueprint('plant', __name__)
requests = []


@plant.route("/water", methods=['POST', 'PUT'])
def water():
    data = http_req.json
    id_s = str(data['serial'])
    req = "w;" + id_s + '.'
    print(req)
    requests.append(req)
    redirect(URL_DASHBOARD + "/plant/" + data['serial'])
    return "ok"


@plant.route("/humidity", methods=['POST', 'PUT'])
def humidity():
    data = http_req.json
    id_s = str(data['serial'])
    req = "h;" + id_s + '.'
    print(req)
    requests.append(req)
    redirect(URL_DASHBOARD + '/plant/' + data['serial'])
    return "ok"
