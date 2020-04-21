from flask import Blueprint, request as http_req, redirect
from constants import URL_DASHBOARD, Operation

request_page = Blueprint('request_page', __name__)
requests = []


@request_blueprint.route("/request", methods=['POST', 'PUT'])
def request():
    global req
    try:
        data = http_req.json
        id_s = str(data['serial'])
        req_type = str(data['request'])

        if req_type == 'water':
            req = str(Operation.WATER.value) + ";" + id_s + '.'

        elif req_type == 'humidity':
            req = str(Operation.HUMIDITY.value) + ";" + id_s + '.'

        elif req_type == 'temperature':
            req = str(Operation.TEMPERATURE.value) + ";" + id_s + '.'

        elif req_type == 'light':
            req = str(Operation.LIGHT.value) + ";" + id_s + '.'

        elif req_type == 'joined':
            req = str(Operation.JOINED.value) + ";" + id_s + '.'

        elif req_type == 'refused':
            req = str(Operation.REFUSED.value) + ";" + id_s + '.'

        requests.append(req)

        return redirect(URL_DASHBOARD + '/plant/' + data['serial'])

    except ValueError:
        pass

