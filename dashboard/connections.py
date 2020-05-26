from flask_login import login_required

from auth import is_admin
from gio_db import delete_conn_req, ConnectionRequest, Radio, url_from_radio
from flask import Blueprint, render_template, redirect, flash
import requests as snd_req
import time

connections_page = Blueprint('connections', __name__)


@connections_page.route("/add_plant_from_conn/<string:idv>/<string:radio_id>", methods=['GET'])
def add_plant_from_conn(idv, radio_id):
    conn = ConnectionRequest.query.filter_by(id=idv, radio_id=radio_id).first()
    if conn is not None:
        url = url_from_radio(radio_id)
        try:
            snd_req.put('http://'+url + '/request', json={'request': 'joined', 'serial': idv})
            time.sleep(2)
            flash('Richiesta inoltrata alla radio con successo', 'success')
        except:
            flash('Impossibile inoltrare la richiesta alla radio - Operazione fallita', 'danger')
    return redirect("/connections")


@connections_page.route("/refuse_plant_from_conn/<string:idv>/<string:radio_id>", methods=['GET'])
def refuse_plant_from_conn(idv,radio_id):
    conn = ConnectionRequest.query.filter_by(id=idv,radio_id=radio_id).first()
    radio = Radio.query.filter_by(id=radio_id)
    if conn is not None:
        url = radio.url_radio
        if url != str(-1):
            try:
                snd_req.put('http://' + url + '/request', json={'request': 'refused', 'serial': idv})
                time.sleep(2)
                flash('Richiesta inoltrata alla radio con successo', 'success')
            except:
                flash('Impossibile inoltrare la richiesta alla radio - Operazione fallita', 'danger')
        else:
            flash('URL della richiesta di connessione non valido... elimino la richiesta', 'warning')
            delete_conn_req(idv=idv, radio=radio_id)
        return redirect("/connections")


@connections_page.route('/connections')
@login_required
def conn_page():
    conn_list = ConnectionRequest.query.all()
    radios = Radio.query.all()
    if is_admin():
        return render_template('connections.html',
                               connections=conn_list,
                               radios = radios,
                               title="Connessioni")
    else:
        flash('Non possiedi i diritti necessari','danger')
        return render_template('connections.html',
                               connections=None,
                               title="Connessioni")
