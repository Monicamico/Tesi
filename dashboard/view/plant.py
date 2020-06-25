from flask import Blueprint, render_template, request as rcv_req, redirect, flash
from flask_login import login_required

from model.forms import PlantForm
from model.gio_db import Plant, url_from_plant, ConnectionRequest
import requests as snd_req
import time

plant_id_page = Blueprint('plant_id_page', __name__)


@plant_id_page.route("/water/<string:idv>", methods=['GET'])
@login_required
def water(idv):
    """
    Send an http request to the radio-raspberry associated with the plant,
    to request the *WATER* Operation

    :param idv: plant serial number
    :type idv: str
    :return: redirect to the plantpage
    :rtype: Response
    """
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
    """
    Send an http request to the radio-raspberry associated with the plant,
    to request the *HUMIDITY* Operation

    :param idv: plant serial number
    :type idv: str
    :return: redirect to the plantpage
    :rtype: Response

    """
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
    """
    Send an http request to the radio-raspberry associated with the plant,
    to request the *TEMPERATURE* Operation

    :param idv: plant serial number
    :type idv: str
    :return: redirect to the plantpage
    :rtype: Response

    """
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
    """
        Send an http request to the radio-raspberry associated with the plant,
        to request the *LIGHT* Operation

        :param idv: plant serial number
        :type idv: str
        :return: redirect to the plantpage
        :rtype: Response

        """
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
    """
        Send an http request to the radio-raspberry associated with the plant,
        to request the *WATER_CONTAINER_STATE* Operation

        :param idv: plant serial number
        :type idv: str
        :return: redirect to the plantpage
        :rtype: Response

        """
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
    """
        Send three http request to the radio-raspberry associated with the plant,
        to request the *TEMPERATURE*, *LIGHT*, *HUMIDITY*  Operations

        :param idv: plant serial number
        :type idv: str
        :return: redirect to the plantpage
        :rtype: Response

        """
    try:
        reply = snd_req.put(str(url_from_plant(idv)) + '/request', json={'request': 'humidity', 'serial': idv})
        print(reply)
        reply = snd_req.put(str(url_from_plant(idv)) + '/request', json={'request': 'light', 'serial': idv})
        print(reply)
        reply = snd_req.put(str(url_from_plant(idv)) + '/request', json={'request': 'temperature', 'serial': idv})
        print(reply)
        flash('Richiesta dello stato della pianta inoltrata alla radio', 'success')
    except:
        flash('Impossibile inoltrare la richiesta alla radio','danger')
        return redirect("/plant/" + idv)
    return redirect("/plant/"+idv)


@plant_id_page.route('/plant/<string:idv>', methods=['POST','GET'])
@login_required
def plant_page(idv):
    """
    Show the plant page with id equal to idv.
    The page will contain the vital values of the plant and buttons
    to modify/delete the plant or request operations on it.

    :param idv: plant serial number
    :type idv: str
    :return: template *plant.html*
    :rtype: template

    """
    form = PlantForm()
    plant_ = Plant.query.filter_by(id=idv).first()
    conn_list = ConnectionRequest.query.all()
    if form.validate_on_submit():
        name = rcv_req.form['name']
        if name == plant_.name:
            try:
                reply = snd_req.put(str(url_from_plant(idv)) + '/request', json={'request': 'deleted', 'serial': idv})
                print(reply)
                time.sleep(3)
                flash('Operazione inoltrata alla radio', 'success')
            except:
                flash("Impossibile eliminare la pianta", 'danger')
                return redirect("/plant/" + idv)
            return redirect("/plants")
        else:
            flash('Il nome della pianta non corrisponde - Pianta non eliminata', 'warning')
            return redirect("/plant/" + idv)

    return render_template('plant.html',
                           form=form,
                           connections=conn_list,
                           plant=plant_,
                           title="Plant")


