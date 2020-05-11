from flask import Blueprint, request as http_req, redirect
from constants import URL_DASHBOARD, Operation, DELIMITER

request_page = Blueprint('request_page', __name__)
request_queue = []


# Request received from dashboard, it will be added to the request queue
@request_page.route("/request", methods=['POST', 'PUT'])
def request():
    global req
    print("Request from dashboard:")
    try:
        data = http_req.json
        id_s = str(data['serial'])
        req_type = str(data['request'])

        if req_type == 'water':
            req = str(Operation.WATER.value) + ";" + id_s + DELIMITER
            print('water')

        elif req_type == 'humidity':
            req = str(Operation.HUMIDITY.value) + ";" + id_s + DELIMITER
            print('humidity')

        elif req_type == 'temperature':
            req = str(Operation.TEMPERATURE.value) + ";" + id_s + DELIMITER
            print('temperature')

        elif req_type == 'light':
            req = str(Operation.LIGHT.value) + ";" + id_s + DELIMITER
            print('light')

        elif req_type == 'joined':
            req = str(Operation.JOINED.value) + ";" + id_s + DELIMITER
            print('joined')

        elif req_type == 'refused':
            req = str(Operation.REFUSED.value) + ";" + id_s + DELIMITER
            print('refused')

        elif req_type == 'vase_state':
            req = str(Operation.VASE_STATE.value) + ";" + id_s + DELIMITER
            print('vase state')

        elif req_type == 'container_state':
            req = str(Operation.WATER_CONTAINER_STATE.value) + ";" + id_s + DELIMITER
            print('container state')

        elif req_type == 'light_max':
            param = str(data['param'])
            req = str(Operation.SET_LIGHT_MAX.value) + ";" + id_s + ";" + param + DELIMITER
            print('light max')

        elif req_type == 'light_min':
            param = str(data['param'])
            req = str(Operation.SET_LIGHT_MIN.value) + ";" + id_s + ";" + param + DELIMITER
            print('light min')

        elif req_type == 'watering_light':
            param = str(data['param'])
            req = str(Operation.SET_WATERING_LIGHT.value) + ";" + id_s + ";" + param + DELIMITER
            print('watering light')

        elif req_type == 'hum_min':
            param = str(data['param'])
            req = str(Operation.SET_HUMIDITY_MIN.value) + ";" + id_s + ";" + param + DELIMITER
            print('humidity min')

        elif req_type == 'hum_max':
            param = str(data['param'])
            req = str(Operation.SET_HUMIDITY_MAX.value) + ";" + id_s + ";" + param + DELIMITER
            print('humidity max')

        elif req_type == 'temp_min':
            param = str(data['param'])
            req = str(Operation.SET_TEMPERATURE_MIN.value) + ";" + id_s + ";" + param + DELIMITER
            print('temperature min')

        elif req_type == 'temp_max':
            param = str(data['param'])
            req = str(Operation.SET_TEMPERATURE_MAX.value) + ";" + id_s + ";" + param + DELIMITER
            print('temperature max')

        request_queue.append(req)
        if req_type == 'joined':
            return redirect(URL_DASHBOARD + '/plants/')
        else:
            return redirect(URL_DASHBOARD + '/plant/' + data['serial'])

    except ValueError:
        pass

