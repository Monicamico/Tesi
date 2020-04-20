from flask import Blueprint, render_template, request as http_req, redirect
from constants import URL_DASHBOARD, Operation

plant = Blueprint('plant', __name__)
requests = []


@plant.route("/request", methods=['POST', 'PUT'])
def request():
    data = http_req.json
    id_s = str(data['serial'])
    req_type = str(data['request'])

    if req_type == 'water':
        req = Operation.WATER + ";" + id_s + '.'
    if req_type == "humidity":
        req = Operation.HUMIDITY + ";" + id_s + '.'
    if req_type == "temperature":
        req = Operation.TEMPERATURE + ";" + id_s + '.'
    if req_type == "light":
        req = Operation.LIGHT + ";" + id_s + '.'
    print(req)
    requests.append(req)
    return redirect(URL_DASHBOARD + '/plant/' + data['serial'])
