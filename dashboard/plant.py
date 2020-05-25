from flask import Blueprint, render_template, request as rcv_req, redirect, flash
from flask_login import login_required

from forms import PlantForm
from gio_db import Plant, url_from_plant, ConnectionRequest, delete_plant
import requests as snd_req
import time

plant_id_page = Blueprint('plant_id_page', __name__)


@plant_id_page.route("/water/<string:idv>", methods=['GET'])
@login_required
def water(idv):
    try:
        reply = snd_req.put(str(url_from_plant(idv)) + '/request', json={"request": "water", "serial": idv})
        print(reply)
        flash('Operazione inoltrata alla radio', 'success')
    except:
        flash("Impossibile inoltrare la richiesta alla radio", 'danger')
        return redirect("/plant/" + idv)
    return redirect("/plant/"+idv)


@plant_id_page.route("/humidity/<string:idv>", methods=['GET'])
@login_required
def humidity(idv):
    try:
        reply = snd_req.put(str(url_from_plant(idv)) + '/request', json={"request": "humidity", "serial": idv})
        print(reply)
        time.sleep(2)
        flash('Operazione inoltrata alla radio', 'success')
    except:
        flash("Impossibile inoltrare la richiesta alla radio",'danger')
        return redirect("/plant/" + idv)
    return redirect("/plant/"+idv)


@plant_id_page.route("/temperature/<string:idv>", methods=['GET'])
@login_required
def temperature(idv):
    try:
        reply = snd_req.put(str(url_from_plant(idv)) + '/request', json={'request': 'temperature', 'serial': idv})
        print(reply)
        time.sleep(2)
        flash('Operazione inoltrata alla radio', 'success')
    except:
        flash("Impossibile inoltrare la richiesta alla radio", 'danger')
        return redirect("/plant/" + idv)
    return redirect("/plant/"+idv)


@plant_id_page.route("/light/<string:idv>", methods=['GET'])
@login_required
def light(idv):
    try:
        reply = snd_req.put(str(url_from_plant(idv)) + '/request', json={'request': 'light', 'serial': idv})
        print(reply)
        time.sleep(2)
        flash('Operazione inoltrata alla radio', 'success')
    except:
        flash("Impossibile inoltrare la richiesta alla radio", 'danger')
        return redirect("/plant/" + idv)
    return redirect("/plant/"+idv)


@plant_id_page.route("/container_state/<string:idv>", methods=['GET'])
@login_required
def container_state(idv):
    try:
        reply = snd_req.put(str(url_from_plant(idv)) + '/request', json={'request': 'container_state', 'serial': idv})
        print(reply)
        flash('Operazione inoltrata alla radio', 'success')
        time.sleep(2)
    except:
        flash("Impossibile inoltrare la richiesta alla radio",'danger')
        return redirect("/plant/" + idv)
    return redirect("/plant/"+idv)


@plant_id_page.route("/vase_state/<string:idv>", methods=['GET'])
@login_required
def vase_state_req(idv):
    try:
        reply = snd_req.put(str(url_from_plant(idv)) + '/request', json={'request': 'humidity', 'serial': idv})
        print(reply)
        reply = snd_req.put(str(url_from_plant(idv)) + '/request', json={'request': 'temperature', 'serial': idv})
        print(reply)
        reply = snd_req.put(str(url_from_plant(idv)) + '/request', json={'request': 'light', 'serial': idv})
        print(reply)
        time.sleep(6)
        flash('Richiesta dello stato della pianta inoltrata alla radio', 'success')

    except:
        flash('Impossibile inoltrare la richiesta alla radio','danger')
        return redirect("/plant/" + idv)
    return redirect("/plant/"+idv)


@plant_id_page.route('/plant/<string:idv>', methods=['POST','GET'])
@login_required
def plant_alert(idv):
    form = PlantForm()
    plant_ = Plant.query.filter_by(id=idv).first()
    conn_list = ConnectionRequest.query.all()
    if form.validate_on_submit():
        name = rcv_req.form['name']
        if name == plant_.name:
            try:
                reply = snd_req.put(str(url_from_plant(idv)) + '/request', json={'request': 'delete', 'serial': idv})
                print(reply)
                time.sleep(2)
                flash('Operazione inoltrata alla radio', 'success')
            except:
                flash("Impossibile eliminare la pianta", 'danger')
                return redirect("/plant/" + idv)
            delete_plant(idv)
            return redirect("/plants/")
        else:
            flash('Il nome della pianta non corrisponde - Pianta non eliminata', 'warning')
            return redirect("/plant/" + idv)

    return render_template('plant.html',
                           form=form,
                           connections=conn_list,
                           plant=plant_,
                           title="Plant")


