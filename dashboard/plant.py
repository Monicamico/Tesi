from flask import Blueprint, render_template, request as rcv_req
from gio_db import Plant, update_hum, update_light, update_temp, update_ping
from constant import URL_RASPBERRY
import requests as snd_req

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


@plant_id_page.route("/water/<string:idv>", methods=['GET'])
def water(idv):
    reply = snd_req.put(URL_RASPBERRY + "/water", json={"serial": idv})
    #if reply.status_code != 200:
        #plant_ = Plant.query.filter_by(id=idv).first()
        #render_template('plant.html',
         #               plant=plant_)
    return plant(idv=idv)


@plant_id_page.route('/plant/<string:idv>')
def plant(idv):
    plant_ = Plant.query.filter_by(id=idv).first()
    return render_template('plant.html',
                           plant=plant_,
                           title="Plant")