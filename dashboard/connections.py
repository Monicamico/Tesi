from gio_db import add_conn_req, delete_conn_req, ConnectionRequest, add_radio, url_from_plant, url_from_conn
from flask import Blueprint, render_template, request as http_req, redirect
import requests as snd_req
from constant import URL
import time

connections_page = Blueprint('connections', __name__)


@connections_page.route("/add_plant_from_conn/<string:idv>", methods=['GET'])
def add_plant_from_conn(idv):
    url = str(url_from_conn(idv))
    print(url)
    plant = ConnectionRequest.query.filter_by(id=idv).first()
    if plant is not None:
        if url != str(-1):
            try:
                snd_req.put(url + '/request', json={'request': 'joined', 'serial': idv})
                time.sleep(2)
                alert = 'add-success'
                return conn_page(alert)
            except:
                print('errore di connessione')
                alert = 'add-fail'
                return conn_page(alert)


@connections_page.route("/refuse_plant_from_conn/<string:idv>", methods=['GET'])
def refuse_plant_from_conn(idv):
    url = str(url_from_conn(idv))
    if url != str(-1):
        try:
            snd_req.put(url + '/request', json={'request': 'refused', 'serial': idv})
            alert = 'refuse-success'
            time.sleep(2)
        except:
            alert = 'refuse-fail'
            print('errore di connessione')
        return conn_page(alert)


@connections_page.route('/connections/<string:alert>')
def conn_page(alert):
    conn_list = ConnectionRequest.query.all()
    return render_template('connections.html',
                           alert=alert,
                           connections=conn_list,
                           title="Connessioni")
