from flask import Blueprint, render_template, request, redirect
from gio_db import Plant, url_from_plant, ConnectionRequest
import requests as snd_req
import time

plant_id_page = Blueprint('plant_id_page', __name__)


@plant_id_page.route("/water/<string:idv>", methods=['GET'])
def water(idv):
    try:
        reply = snd_req.put(str(url_from_plant(idv)) + '/request', json={"request": "water", "serial": idv})
        print(reply)
        alert='success'
    except:
        print('errore di connessione con RaspberryFlask')
        alert = 'fail'
    return redirect("/plant/"+idv+"/"+alert)


@plant_id_page.route("/humidity/<string:idv>", methods=['GET'])
def humidity(idv):
    try:
        reply = snd_req.put(str(url_from_plant(idv)) + '/request', json={"request": "humidity", "serial": idv})
        print(reply)
        time.sleep(2)
        alert = 'success'
    except:
        print('errore di connessione con RaspberryFlask')
        alert = 'fail'
    return redirect("/plant/"+idv+"/"+alert)


@plant_id_page.route("/temperature/<string:idv>", methods=['GET'])
def temperature(idv):
    try:
        reply = snd_req.put(str(url_from_plant(idv)) + '/request', json={'request': 'temperature', 'serial': idv})
        print(reply)
        time.sleep(2)
        alert = 'success'
    except:
        print('errore di connessione con RaspberryFlask')
        alert = 'fail'
    return redirect("/plant/"+idv+"/"+alert)


@plant_id_page.route("/light/<string:idv>", methods=['GET'])
def light(idv):
    try:
        reply = snd_req.put(str(url_from_plant(idv)) + '/request', json={'request': 'light', 'serial': idv})
        print(reply)
        time.sleep(2)
        alert = 'success'
    except:
        print('errore di connessione con RaspberryFlask')
        alert = 'fail'
    return redirect("/plant/"+idv+"/"+alert)


@plant_id_page.route("/container_state/<string:idv>", methods=['GET'])
def container_state(idv):
    try:
        reply = snd_req.put(str(url_from_plant(idv)) + '/request', json={'request': 'container_state', 'serial': idv})
        print(reply)
        time.sleep(2)
        alert = 'success'
    except:
        alert = 'fail'
        print('errore di connessione con RaspberryFlask')
    return redirect("/plant/"+idv+"/"+alert)


@plant_id_page.route("/vase_state/<string:idv>", methods=['GET'])
def vase_state_req(idv):
    alert = 'success'
    try:
        reply = snd_req.put(str(url_from_plant(idv)) + '/request', json={'request': 'vase_state', 'serial': idv})
        print(reply)
        time.sleep(2)
    except:
        alert = 'fail'
        print('errore di connessione con RaspberryFlask')
    return redirect("/plant/"+idv+"/"+alert)


@plant_id_page.route('/plant/<string:idv>/<string:alert>')
def plant_alert(idv, alert):
    plant_ = Plant.query.filter_by(id=idv).first()
    conn_list = ConnectionRequest.query.all()
    return render_template('plant.html',
                           alert=alert,
                           connections=conn_list,
                           plant=plant_,
                           title="Plant")


