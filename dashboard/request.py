from flask import Blueprint, request as rcv_req, redirect, flash
from gio_db import add_radio, add_conn_req, delete_conn_req, \
    add_plant, delete_plant, \
    update_hum, update_light, update_temp, \
    update_ping, update_water_container_state, \
    update_hum_min, update_hum_max, \
    update_light_min, update_light_max, \
    update_temp_min, update_temp_max, \
    update_watering_light, \
    update_vase_transmit_power, update_radio_transmit_power, update_water_container_size, \
    update_send_time, update_sleep_time, update_plant_state_fitness
from constant import Operation

request_page = Blueprint('request_page', __name__)


# Request or response received from raspberry(RADIO)
@request_page.route("/request", methods=['POST', 'PUT'])
def request():
    data = rcv_req.json
    try:
        req = int(data['request'])
        print(req)
    except:
        return "500"

    if req == Operation.RADIO_JOIN.value:
        add_radio(data['serial'], data['url'])
        return redirect("/home")

    elif req == Operation.CONNECTION.value:
        ping = data['ping']
        param = data['param']
        url = data['url']
        add_conn_req(data['serial'], ping, param, url)
        return redirect("/home")

    elif req == Operation.REFUSED.value:
        delete_conn_req(data['serial'])

    elif req == Operation.JOINED.value:
        try:
            ping = data['ping']
            param = data['param']
            add_plant(data['serial'], ping, param)
        except:
            print("Join: error")

    elif req == Operation.DELETED.value:
        delete_plant(data['serial'])

    elif req == Operation.HUMIDITY.value:
        try:
            serial_number = data['serial']
            ping = data['ping']
            param = data['param']
            update_hum(serial_number, ping, param)
        except:
            print("Humidity: error")
        try:
            update_plant_state_fitness(serial_number)
        except:
            print("Humidity, state update: error")

    elif req == Operation.LIGHT.value:
        try:
            serial_number = data['serial']
            ping = data['ping']
            param = data['param']
            update_light(serial_number, ping, param)
        except:
            print("Light: error")
        try:
            update_plant_state_fitness(serial_number)
        except:
            print("Light, state update: error")

    elif req == Operation.TEMPERATURE.value:
        try:
            serial_number = data['serial']
            ping = data['ping']
            param = data['param']
            update_temp(serial_number, ping, param)
        except:
            pass
        try:
            update_plant_state_fitness(serial_number)
        except:
            print("Temperature, state update: error")

    elif req == Operation.PING.value:
        try:
            serial_number = data['serial']
            ping = data['ping']
            update_ping(serial_number, ping)
        except:
            print()

    elif req == Operation.SET_WATERING_LIGHT.value:
        try:
            serial_number = data['serial']
            ping = data['ping']
            param = data['param']
            update_watering_light(serial_number, ping, param)
        except:
            print()

    elif req == Operation.WATER_CONTAINER_STATE.value:
        try:
            serial_number = data['serial']
            ping = data['ping']
            param = data['param']
            update_water_container_state(serial_number, ping, param)
        except:
            print()

    elif req == Operation.SET_WATER_CONTAINER_SIZE.value:
        try:
            serial_number = data['serial']
            ping = data['ping']
            param = data['param']
            update_water_container_size(serial_number, ping, param)
        except:
            print()

    elif req == Operation.SET_HUMIDITY_MIN.value:
        try:
            serial_number = data['serial']
            ping = data['ping']
            param = data['param']
            update_hum_min(serial_number, ping, param)
        except:
            print()
        try:
            update_plant_state_fitness(serial_number)
        except:
            print("Update-state_fitness: error")

    elif req == Operation.SET_HUMIDITY_MAX.value:
        try:
            serial_number = data['serial']
            ping = data['ping']
            param = data['param']
            update_hum_max(serial_number, ping, param)
        except:
            print()
        try:
            update_plant_state_fitness(serial_number)
        except:
            print("Update-state_fitness: error")

    elif req == Operation.SET_LIGHT_MIN.value:
        try:
            serial_number = data['serial']
            ping = data['ping']
            param = data['param']
            update_light_min(serial_number,ping, param)
        except:
            print()
        try:
            update_plant_state_fitness(serial_number)
        except:
            print("Update-state_fitness: error")

    elif req == Operation.SET_LIGHT_MAX.value:
        try:
            serial_number = data['serial']
            ping = data['ping']
            param = data['param']
            update_light_max(serial_number, ping, param)
        except:
            print()
        try:
            update_plant_state_fitness(serial_number)
        except:
            print("Update-state_fitness: error")

    elif req == Operation.SET_TEMPERATURE_MIN.value:
        try:
            serial_number = data['serial']
            ping = data['ping']
            param = data['param']
            update_temp_min(serial_number, ping, param)
        except:
            print()
        try:
            update_plant_state_fitness(serial_number)
        except:
            print("Update-state_fitness: error")

    elif req == Operation.SET_TEMPERATURE_MAX.value:
        try:
            serial_number = data['serial']
            ping = data['ping']
            param = data['param']
            update_temp_max(serial_number, ping, param)
        except:
            print()
        try:
            update_plant_state_fitness(serial_number)
        except:
            print("Update-state_fitness: error")

    elif req == Operation.VASE_TRANSMIT_POWER.value:
        try:
            serial_number = data['serial']
            ping = data['ping']
            param = data['param']
            update_vase_transmit_power(serial_number,param)
        except:
            print()

    elif req == Operation.RADIO_TRANSMIT_POWER.value:
        try:
            serial_number = data['serial']
            param = data['param']
            update_radio_transmit_power(serial_number, param)
        except:
            print()

    elif req == Operation.SET_VASE_SEND_TIME.value:
        try:
            serial_number = data['serial']
            param = data['param']
            update_send_time(serial_number, param)
        except:
            print()

    elif req == Operation.SET_RADIO_PAUSE_TIME.value:
        try:
            serial_number = data['serial']
            param = data['param']
            update_sleep_time(serial_number, param)
        except:
            print()

    return "200"