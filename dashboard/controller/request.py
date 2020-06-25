from flask import Blueprint, request as rcv_req
import requests as snd_req
from controller.utility import add_conn_req, delete_conn_req, update_sleep_time, update_radio_transmit_power, add_radio, \
    radio_from_url, associated_plants, add_plant, delete_plant, update_vase_transmit_power, update_send_time, \
    update_hum, update_temp, update_light, update_plant_state_fitness, update_temp_min, update_temp_max, update_hum_min, \
    update_hum_max, update_light_max, update_light_min, update_watering_light, update_water_container_size, \
    update_water_container_state
from model.constant import Operation

request_page = Blueprint('request_page', __name__)


# Request or response received from raspberry(RADIO)
@request_page.route("/request", methods=['POST', 'PUT'])
def request():
    """
        *Recive a request or response from a Radio-Raspberry*

        **Data received:**
            - data['request']
            - data['serial']

        **Optional Data received:**
            - data['signal']
            - data['param']
            - data['url']

        **Types of request:**

            - Operation.RADIO_JOIN:

                call the func. *add_radio(id, url)*, the id and url are data (json) received from the
                radio-raspberry, and if the radio has associated vases, send an http request to send
                information about them, so that the radio can add them to the list.

            - Operation.CONNECTION

                call the func. *add_conn_req* with the received data.

            - Operation.REFUSED

                call the func. *delete_conn_req*

            - Operation.JOINED

                 call the func. *add_plant*

            - Operation.DELETED

                call the func. *delete_plant*

            - Operation.HUMIDITY

                 call the func. *update_hum(serial, param)* and *update_plant_state_fitness(serial)*

            - Operation.LIGHT

                call the func. *update_light(serial, param)* and *update_plant_state_fitness(serial)*

            - Operation.TEMPERATURE

                call the func. *update_temp(serial, param)* and *update_plant_state_fitness(serial)*

            - Operation.SET_WATERING_LIGHT

                call the func. *update_watering_light(serial, param)*

            - Operation.WATER_CONTAINER_STATE

                call the func. *update_water_container_state(serial, param)*

            - Operation.SET_WATER_CONTAINER_SIZE

                call the func. *update_water_container_size(serial, param)*

            - Operation.SET_HUMIDITY_MIN

                call the func. *update_hum_min(serial, param)* and *update_plant_state_fitness(serial)*

            - Operation.SET_HUMIDITY_MAX

                 call the func. *update_hum_max(serial, param)* and *update_plant_state_fitness(serial)*

            - Operation.SET_LIGHT_MIN

                 call the func. *update_light_min(serial, param)* and *update_plant_state_fitness(serial)*

            - Operation.SET_LIGHT_MAX

                 call the func. *update_light_max(serial, param)* and *update_plant_state_fitness(serial)*

            - Operation.SET_TEMPERATURE_MIN

                 call the func. *update_temp_min(serial, param)* and *update_plant_state_fitness(serial)*

            - Operation.SET_TEMPERATURE_MAX

                 call the func. *update_temp_max(serial, param)* and *update_plant_state_fitness(serial)*

            - Operation.VASE_TRANSMIT_POWER

                 call the func. *update_vase_transmit_power(serial, param)*

            - Operation.RADIO_TRANSMIT_POWER

                 call the func. *update_radio_transmit_power(serial, param)*

            - Operation.SET_VASE_SEND_TIME

                 call the func. *update_send_time(serial, param)*

            - Operation.SET_RADIO_PAUSE_TIME

                 call the func. *update_sleep_time(serial, param)*

    """
    data = rcv_req.json
    try:
        req = int(data['request'])
        print(req)
    except:
        return "500"

    if req == Operation.RADIO_JOIN.value:
        radio_id = data['serial']
        url = data['url']
        if add_radio(radio_id, url) is False:
            plants = associated_plants(radio_id)
            if plants is not None:
                for plant in plants:
                    snd_req.put('http://' + url + '/request', json={'request': 'existing_vase', 'serial': plant.id})

    elif req == Operation.CONNECTION.value:
        signal = data['signal']
        param = data['param']
        url = data['url']
        r = radio_from_url(url)
        if add_conn_req(data['serial'], signal, param, r.id) is True:
            return "200"

    elif req == Operation.REFUSED.value:
        radio = radio_from_url(data['url'])
        delete_conn_req(data['serial'], radio.id)

    elif req == Operation.JOINED.value:
        param = data['param']
        add_plant(data['serial'],param)

    elif req == Operation.DELETED.value:
        delete_plant(data['serial'])

    elif req == Operation.HUMIDITY.value:
        serial_number = data['serial']
        param = data['param']
        update_hum(serial_number, param)
        try:
            update_plant_state_fitness(serial_number)
        except:
            print("Humidity, state update: error")

    elif req == Operation.LIGHT.value:
        serial_number = data['serial']
        param = int(data['param'])
        update_light(serial_number, param)
        try:
            update_plant_state_fitness(serial_number)
        except:
            print("Light, state update: error")

    elif req == Operation.TEMPERATURE.value:
        serial_number = data['serial']
        param = data['param']
        update_temp(serial_number, param)
        try:
            update_plant_state_fitness(serial_number)
        except:
            print("Temperature, state update: error")

    elif req == Operation.SET_WATERING_LIGHT.value:
        serial_number = data['serial']
        param = data['param']
        update_watering_light(serial_number, param)

    elif req == Operation.WATER_CONTAINER_STATE.value:
        serial_number = data['serial']
        param = data['param']
        update_water_container_state(serial_number,  param)

    elif req == Operation.SET_WATER_CONTAINER_SIZE.value:
        serial_number = data['serial']
        param = data['param']
        update_water_container_size(serial_number, param)

    elif req == Operation.SET_HUMIDITY_MIN.value:
        serial_number = data['serial']
        param = data['param']
        update_hum_min(serial_number, param)
        try:
            update_plant_state_fitness(serial_number)
        except:
            print("Update-state_fitness: error")

    elif req == Operation.SET_HUMIDITY_MAX.value:
        serial_number = data['serial']
        param = data['param']
        update_hum_max(serial_number, param)
        try:
            update_plant_state_fitness(serial_number)
        except:
            print("Update-state_fitness: error")

    elif req == Operation.SET_LIGHT_MIN.value:
        serial_number = data['serial']
        param = data['param']
        update_light_min(serial_number, param)
        try:
            update_plant_state_fitness(serial_number)
        except:
            print("Update-state_fitness: error")

    elif req == Operation.SET_LIGHT_MAX.value:
        serial_number = data['serial']
        param = data['param']
        update_light_max(serial_number, param)
        try:
            update_plant_state_fitness(serial_number)
        except:
            print("Update-state_fitness: error")

    elif req == Operation.SET_TEMPERATURE_MIN.value:
        try:
            serial_number = data['serial']
            param = data['param']
            update_temp_min(serial_number, param)
        except:
            print()
        try:
            update_plant_state_fitness(serial_number)
        except:
            print("Update-state_fitness: error")

    elif req == Operation.SET_TEMPERATURE_MAX.value:
        try:
            serial_number = data['serial']
            param = data['param']
            update_temp_max(serial_number, param)
        except:
            print()
        try:
            update_plant_state_fitness(serial_number)
        except:
            print("Update-state_fitness: error")

    elif req == Operation.VASE_TRANSMIT_POWER.value:
        try:
            serial_number = data['serial']
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