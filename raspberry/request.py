from flask import Blueprint, request as http_req, redirect
from constants import URL_DASHBOARD, Operation, DELIMITER
from utility import lock_queue, condition_variable

request_page = Blueprint('request_page', __name__)
request_queue = []


# Request received from DASHBOARD Server, it will be added to the request queue
@request_page.route("/request", methods=['POST', 'PUT'])
def request():
    """
    Reads the received request from the dashobard server and adds that to the request queue.
    """
    global req
    print("Request from dashboard:")
    try:
        data = http_req.json
        id_s = str(data['serial'])
        req_type = str(data['request'])

        if req_type == 'water':
            req = str(Operation.WATER.value) + ";" + id_s + DELIMITER
            print('water / '+id_s)

        elif req_type == 'humidity':
            req = str(Operation.HUMIDITY.value) + ";" + id_s + DELIMITER
            print('humidity / ' + id_s)

        elif req_type == 'temperature':
            req = str(Operation.TEMPERATURE.value) + ";" + id_s + DELIMITER
            print('temperature / ' + id_s)

        elif req_type == 'light':
            req = str(Operation.LIGHT.value) + ";" + id_s + DELIMITER
            print('light / ' + id_s)

        elif req_type == 'joined':
            req = str(Operation.JOINED.value) + ";" + id_s + DELIMITER
            print('joined / '+id_s)

        elif req_type == 'deleted':
            req = str(Operation.DELETED.value) + ";" + id_s + DELIMITER
            print('deleted / '+id_s)

        elif req_type == 'refused':
            req = str(Operation.REFUSED.value) + ";" + id_s + DELIMITER
            print('refused / '+id_s)

        elif req_type == 'container_state':
            req = str(Operation.WATER_CONTAINER_STATE.value) + ";" + id_s + DELIMITER
            print('container state / '+id_s)

        elif req_type == 'light_max':
            param = str(data['param'])
            req = str(Operation.SET_LIGHT_MAX.value) + ";" + id_s + ";" + param + DELIMITER
            print('light max / '+ id_s)

        elif req_type == 'light_min':
            param = str(data['param'])
            req = str(Operation.SET_LIGHT_MIN.value) + ";" + id_s + ";" + param + DELIMITER
            print('light min / '+id_s)

        elif req_type == 'watering_light':
            param = str(data['param'])
            req = str(Operation.SET_WATERING_LIGHT.value) + ";" + id_s + ";" + param + DELIMITER
            print('watering light / '+id_s)

        elif req_type == 'hum_min':
            param = str(data['param'])
            req = str(Operation.SET_HUMIDITY_MIN.value) + ";" + id_s + ";" + param + DELIMITER
            print('humidity min / '+id_s)

        elif req_type == 'hum_max':
            param = str(data['param'])
            req = str(Operation.SET_HUMIDITY_MAX.value) + ";" + id_s + ";" + param + DELIMITER
            print('humidity max')

        elif req_type == 'temp_min':
            param = str(data['param'])
            req = str(Operation.SET_TEMPERATURE_MIN.value) + ";" + id_s + ";" + param + DELIMITER
            print('temperature min / '+id_s)

        elif req_type == 'temp_max':
            param = str(data['param'])
            req = str(Operation.SET_TEMPERATURE_MAX.value) + ";" + id_s + ";" + param + DELIMITER
            print('temperature max / '+id_s)

        elif req_type == 'water_container_size':
            param = str(data['param'])
            req = str(Operation.SET_WATER_CONTAINER_SIZE.value) + ";" + id_s + ";" + param + DELIMITER
            print('water_container_size / '+id_s)

        elif req_type == 'vase_transmit_power':
            param = str(data['param'])
            req = str(Operation.VASE_TRANSMIT_POWER.value) + ";" + id_s + ";" + param + DELIMITER
            print('vase_transmit_power / '+ id_s + " / " + param)

        elif req_type == 'radio_transmit_power':
            param = str(data['param'])
            req = str(Operation.RADIO_TRANSMIT_POWER.value) + ";" + id_s + ";" + param + DELIMITER
            print('radio_transmit_power / '+id_s + " / " + param)

        elif req_type == 'send_time':
            param = str(data['param'])
            req = str(Operation.SET_VASE_SEND_TIME.value) + ";" + id_s + ";" + param + DELIMITER
            print('vase send_time / '+id_s)

        elif req_type == 'sleep_time':
            param = str(data['param'])
            req = str(Operation.SET_RADIO_PAUSE_TIME.value) + ";" + id_s + ";" + param + DELIMITER
            print('radio sleep_time / '+id_s)

        elif req_type == 'existing_vase':
            req = str(Operation.ADD_EXISTING_VASE.value) + ";" + id_s + ";" + DELIMITER
            print('existing_vase / '+id_s)

        lock_queue.acquire()
        request_queue.append(req)
        condition_variable.notify_all()
        lock_queue.release()
        return "200"

    except ValueError:
        pass

