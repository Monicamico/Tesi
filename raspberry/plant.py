from flask import Blueprint, render_template, request as http_req, redirect
from constants import URL_DASHBOARD, Operation

plant = Blueprint('plant', __name__)
requests = []


@plant.route("/request", methods=['POST', 'PUT'])
def request():
    try:
        data = http_req.json
        id_s = str(data['serial'])
        req_type = str(data['request'])

        if req_type == 'water':
            req = str(Operation.WATER.value) + ";" + id_s + '.'
        if req_type == "humidity":
            req = str(Operation.HUMIDITY.value) + ";" + id_s + '.'
        if req_type == "temperature":
            req = str(Operation.TEMPERATURE.value) + ";" + id_s + '.'
        if req_type == "light":
            req = str(Operation.LIGHT.value) + ";" + id_s + '.'
        requests.append(req)
        return redirect(URL_DASHBOARD + '/plant/' + data['serial'])

    except ValueError:
        pass

