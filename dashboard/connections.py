from gio_db import add_conn_req, delete_conn_req, ConnectionRequest, add_radio
from flask import Blueprint, render_template, request as http_req, redirect
import requests as snd_req
from constant import URL_RASPBERRY, URL
import time

connections_page = Blueprint('connections', __name__)


@connections_page.route("/radio_conn_request", methods=['POST', 'PUT'])
def radio_conn_req():
    data = http_req.json
    add_radio(data['serial'], data['url'])
    return 'ok'


@connections_page.route("/add_conn_request", methods=['POST', 'PUT'])
def conn_req():
    data = http_req.json
    add_conn_req(data['serial'], data['ping'], data['pairing'])
    return 'ok'


@connections_page.route("/delete_conn_request", methods=['POST', 'PUT'])
def del_conn_req():
    data = http_req.json
    delete_conn_req(data['serial'])
    return "ok"


@connections_page.route("/add_plant_from_conn/<string:idv>", methods=['GET'])
def add_plant_from_conn(idv):
    plant = delete_conn_req(idv=idv)
    if plant is None:
        return redirect(URL+'/connections')
    reply = snd_req.put(URL_RASPBERRY + '/request', json={'request': 'joined', 'serial': idv})
    print(reply)
    time.sleep(2)
    return redirect(URL+'/plants')


@connections_page.route("/refuse_plant_from_conn/<string:idv>", methods=['GET'])
def refuse_plant_from_conn(idv):
    reply = snd_req.put(URL_RASPBERRY + '/request', json={'request': 'refused', 'serial': idv})
    print(reply)
    time.sleep(2)
    return redirect(URL+'/connections')


@connections_page.route('/connections')
def conn_page():
    conn_list = ConnectionRequest.query.all()
    return render_template('connections.html',
                           connections=conn_list,
                           title="Gio-Vase")
