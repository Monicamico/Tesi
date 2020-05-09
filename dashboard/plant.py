from flask import Blueprint, render_template, request as rcv_req, redirect
from gio_db import Plant, update_hum, update_light, update_temp, update_ping, update_water_container_state, \
    update_vase_state
from constant import URL_RASPBERRY, URL
import requests as snd_req
import time

plant_id_page = Blueprint('plant_id_page', __name__)


@plant_id_page.route("/update_hum", methods=['POST', 'PUT'])
def update_plant_hum():
    data = rcv_req.json
    update_hum(data['serial'], data['ping'], data['hum'])
    return "ok"


@plant_id_page.route("/update_temp", methods=['POST', 'PUT'])
def update_plant_temp():
    data = rcv_req.json
    update_temp(data['serial'], data['ping'], data['temp'])
    return "ok"


@plant_id_page.route("/update_light", methods=['POST', 'PUT'])
def update_plant_light():
    data = rcv_req.json
    update_light(data['serial'], data['ping'], data['light'])
    return "ok"


@plant_id_page.route("/update_ping", methods=['POST', 'PUT'])
def update_plant_ping():
    data = rcv_req.json
    update_ping(data['serial'], data['ping'])
    return "ok"


@plant_id_page.route("/update_water_container_state", methods=['POST', 'PUT'])
def update_water_container_state():
    data = rcv_req.json
    update_water_container_state(data['serial'], data['ping'], data['state'])
    return "ok"


@plant_id_page.route("/update_vase_state", methods=['POST', 'PUT'])
def update_vase_state():
    data = rcv_req.json
    update_vase_state(data['serial'], data['ping'], data['state'])
    return "ok"


@plant_id_page.route("/water/<string:idv>", methods=['GET'])
def water(idv):
    try:
        reply = snd_req.put(URL_RASPBERRY + '/request', json={"request": "water", "serial": idv})
        print(reply)
    except snd_req.exceptions.ConnectionError:
        print('errore di connessione con RaspberryFlask')
    return redirect(URL+'/plant/'+str(idv))


@plant_id_page.route("/humidity/<string:idv>", methods=['GET'])
def humidity(idv):
    try:
        reply = snd_req.put(URL_RASPBERRY + '/request', json={"request": "humidity", "serial": idv})
        print(reply)
        time.sleep(2)
    except snd_req.exceptions.ConnectionError:
        print('errore di connessione con RaspberryFlask')
    return redirect(URL+'/plant/'+str(idv))


@plant_id_page.route("/temperature/<string:idv>", methods=['GET'])
def temperature(idv):
    try:
        reply = snd_req.put(URL_RASPBERRY + '/request', json={'request': 'temperature', 'serial': idv})
        print(reply)
        time.sleep(2)
    except snd_req.exceptions.ConnectionError:
        print('errore di connessione con RaspberryFlask')
    return redirect(URL+'/plant/'+str(idv))


@plant_id_page.route("/light/<string:idv>", methods=['GET'])
def light(idv):
    try:
        reply = snd_req.put(URL_RASPBERRY + '/request', json={'request': 'light', 'serial': idv})
        print(reply)
        time.sleep(2)
    except snd_req.exceptions.ConnectionError:
        print('errore di connessione con RaspberryFlask')
    return redirect(URL+'/plant/'+str(idv))


@plant_id_page.route("/container_state/<string:idv>", methods=['GET'])
def container_state(idv):
    try:
        reply = snd_req.put(URL_RASPBERRY + '/request', json={'request': 'container_state', 'serial': idv})
        print(reply)
        time.sleep(2)
    except snd_req.exceptions.ConnectionError:
        print('errore di connessione con RaspberryFlask')
    return redirect(URL+'/plant/'+str(idv))


@plant_id_page.route("/vase_state/<string:idv>", methods=['GET'])
def vase_state_req(idv):
    try:
        reply = snd_req.put(URL_RASPBERRY + '/request', json={'request': 'vase_state', 'serial': idv})
        print(reply)
        time.sleep(2)
    except snd_req.exceptions.ConnectionError:
        print('errore di connessione con RaspberryFlask')
    return redirect(URL+'/plant/'+str(idv))


@plant_id_page.route('/plant/<string:idv>')
def plant(idv):
    plant_ = Plant.query.filter_by(id=idv).first()
    return render_template('plant.html',
                           plant=plant_,
                           title="Plant")