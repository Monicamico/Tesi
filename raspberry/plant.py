from flask import Blueprint, render_template, request as http_req, redirect
from costants import URL_DASHBOARD

plant = Blueprint('plant', __name__)
requests = []


@plant.route("/request", methods=['POST', 'PUT'])
def request():
    data = http_req.json
    id_s = str(data['serial'])
    req_type = str(data['request'])

    if req_type == 'water':
        req = "w;" + id_s + '.'
    if req_type == "humidity":
        req = "h;" + id_s + '.'
    if req_type == "temperature":
        req = "t;" + id_s + '.'
    if req_type == "light":
        req = "l;" + id_s + '.'
    print(req)
    requests.append(req)
    redirect(URL_DASHBOARD + '/plant/' + data['serial'])
    return '200'
