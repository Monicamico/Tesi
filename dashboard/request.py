from flask import Blueprint, request as rcv_req
from gio_db import add_radio, add_conn_req, delete_conn_req, \
    add_plant, delete_plant, \
    update_hum, update_light, update_temp, \
    update_ping, update_water_container_state, update_vase_state, \
    update_hum_min, update_hum_max, \
    update_light_min, update_light_max, \
    update_temp_min, update_temp_max, \
    update_watering_light, update_vase_transmit_power, update_radio_transmit_power
from constant import Operation

request_page = Blueprint('request_page', __name__)


# request or response received from raspberry
@request_page.route("/request", methods=['POST', 'PUT'])
def request():
    data = rcv_req.json

    req = int(data['request'])
    serial_number = data['serial']
    ping = data['ping']
    url = data['url']
    param = int(data['param'])

    if req == Operation.RADIO_JOIN.value:
        add_radio(serial_number, url)

    elif req == Operation.CONNECTION.value:
        add_conn_req(serial_number, ping, param, url)

    elif req == Operation.REFUSED.value:
        delete_conn_req(serial_number)

    elif req == Operation.JOINED.value:
        add_plant(serial_number, ping, param)

    elif req == Operation.DELETED.value:
        delete_plant(serial_number)

    elif req == Operation.HUMIDITY.value:
        update_hum(serial_number, ping, param)

    elif req == Operation.LIGHT.value:
        update_light(serial_number, ping, param)

    elif req == Operation.TEMPERATURE.value:
        update_temp(serial_number, ping, param)

    elif req == Operation.PING.value:
        update_ping(serial_number, ping)

    elif req == Operation.SET_WATERING_LIGHT.value:
        update_watering_light(serial_number, ping, param)

    elif req == Operation.WATER_CONTAINER_STATE.value:
        update_water_container_state(serial_number, ping, param)

    elif req == Operation.VASE_STATE.value:
        update_vase_state(serial_number, ping, param)

    elif req == Operation.SET_HUMIDITY_MIN.value:
        update_hum_min(serial_number, ping, param)

    elif req == Operation.SET_HUMIDITY_MAX.value:
        update_hum_max(serial_number, ping, param)

    elif req == Operation.SET_LIGHT_MIN.value:
        update_light_min(serial_number,ping, param)

    elif req == Operation.SET_LIGHT_MAX.value:
        update_light_max(serial_number, ping, param)

    elif req == Operation.SET_TEMPERATURE_MIN.value:
        update_temp_min(serial_number, ping, param)

    elif req == Operation.SET_TEMPERATURE_MAX.value:
        update_temp_max(serial_number, ping, param)

    elif req == Operation.VASE_TRANSMIT_POWER.value:
        update_vase_transmit_power(serial_number,param)

    elif req == Operation.RADIO_TRANSMIT_POWER.value:
        update_radio_transmit_power(serial_number, param)

    return "200"