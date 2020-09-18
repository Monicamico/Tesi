from flask_login import login_required
from flask import Blueprint, render_template, flash, request as rcv_req, redirect
from view.login import is_admin
from model.forms import SettingsForm
from model.gio_db import Plant, ConnectionRequest, TypePlant
from controller.utility import url_from_plant, update_name, change_type, update_ideal_hum, update_ideal_light, \
    update_ideal_temp
import time
import requests as snd_req

settings_page = Blueprint('settings_page', __name__)


@settings_page.route('/settings/<string:idv>', methods=['POST', 'GET'])
@login_required
def settings(idv):
    """
    If the current user is admin, show the plant settings.

    :param idv: plant serial number
    :type idv: str
    :return: template *plant_settings.html* or *error.html*
    :rtype: template

    """
    if is_admin():
        plant_s = Plant.query.filter_by(id=idv).first()
        conn_list = ConnectionRequest.query.all()
        type_list = TypePlant.query.all()
        settings_form = SettingsForm()
        URL_RASPBERRY = str(url_from_plant(idv))
        if URL_RASPBERRY == str(-1):
            flash('Errore sull indirizzo della radio ', 'danger')
            return redirect("settings/" + idv)

        if settings_form.validate_on_submit():
            name = rcv_req.form['name']
            light_max = round(int(rcv_req.form['light_max']) / 100 * 255)
            light_min = round(int(rcv_req.form['light_min']) / 100 * 255)
            temp_max = int(rcv_req.form['temp_max'])
            temp_min = int(rcv_req.form['temp_min'])
            ideal_t = int(rcv_req.form['ideal_t'])
            ideal_l = round(int(rcv_req.form['ideal_l']) / 100 * 255)
            hum_min = round(int(rcv_req.form['hum_min']) / 100 * 1023)
            hum_max = round(int(rcv_req.form['hum_max']) / 100 * 1023)
            ideal_h = round(int(rcv_req.form['ideal_h']) / 100 * 1023)
            typeplant_id = rcv_req.form['typeplant_id']
            watering_light = round(int(rcv_req.form['watering_light']) / 100 * 255)
            water_container_size = rcv_req.form['water_container_size']
            transmit_power = int(rcv_req.form.get('transmit_power'))
            send_time = int(rcv_req.form.get('send_time'))

            if name != plant_s.name:
                if update_name(idv, name):
                    flash('Nome della pianta cambiato con successo', 'success')
                else:
                    flash('Impossibile cambiare il nome della pianta - possibile duplicato', 'danger')

            if typeplant_id != plant_s.typeplant_id:
                if change_type(idv, typeplant_id, URL_RASPBERRY):
                    flash('Tipo della pianta cambiato con successo', 'success')
                    return redirect('/settings/' + idv)
                else:
                    flash('Impossibile cambiare il tipo della pianta - Radio non raggiungibile', 'warning')
                return redirect('/settings/' + idv)

            if ideal_h != plant_s.ideal_h:
                if 0 <= ideal_h <= 1023 and hum_min <= ideal_h <= hum_max:
                    update_ideal_hum(plant_s.id, ideal_h)
                else:
                    flash('Controlla che il valore sia tra lo 0% e il 100% e che il valore sia compreso tra il min e il max', 'warning')

            if ideal_t != plant_s.ideal_t and temp_min <= ideal_t <= temp_max:
                update_ideal_temp(plant_s.id, ideal_t)

            if ideal_l != plant_s.ideal_l and light_min <= ideal_l <= light_max:
                if 0 <= ideal_h <= 255:
                    update_ideal_light(plant_s.id, ideal_l)
                else:
                    flash('Controlla che il valore sia tra lo 0% e il 100% e che il valore sia compreso tra il min e il max', 'warning')

            if light_max != plant_s.light_max:
                if 0 <= light_max <= 255:
                    try:
                        snd_req.put(URL_RASPBERRY + '/request', json=dict(request='light_max', serial=idv, param=light_max))
                    except:
                        flash('Impossible inoltrare la richiesta', 'danger')
                else:
                    flash('Controlla che il valore sia tra lo 0% e il 100%', 'warning')

            if light_min != plant_s.light_min:
                if 0 <= light_min <= 255:
                    try:
                        snd_req.put(URL_RASPBERRY + '/request',
                                    json={'request': 'light_min', 'serial': idv, 'param': light_min})
                    except:
                        flash('Impossible inoltrare la richiesta', 'danger')
                        return redirect('/settings/' + idv)
                else:
                    flash('Controlla che il valore sia tra lo 0% e il 100% - (Luce massima)', 'warning')

            if watering_light != plant_s.watering_light:
                if 0 <= watering_light <= 255:
                    try:
                        snd_req.put(URL_RASPBERRY + '/request',
                                    json={'request': 'watering_light', 'serial': idv, 'param': watering_light})
                    except:
                        flash('Impossible inoltrare la richiesta', 'danger')
                else:
                    flash('Controlla che il valore sia tra lo 0% e il 100% - (Luce per innaffiare)', 'warning')

            if hum_min != plant_s.humidity_min:
                if 0 <= hum_min <= 1023:
                    try:
                        snd_req.put(URL_RASPBERRY + '/request', json={'request': 'hum_min', 'serial': idv, 'param': hum_min})
                    except:
                        flash('Impossible inoltrare la richiesta', 'danger')
                else:
                    flash('Controlla che il valore sia tra lo 0% e il 100% - (Umidita minima)', 'warning')

            if hum_max != plant_s.humidity_max:
                if 0 <= hum_max <= 1023:
                    try:
                        snd_req.put(URL_RASPBERRY + '/request', json={'request': 'hum_max', 'serial': idv, 'param': hum_max})
                    except:
                        flash('Impossible inoltrare la richiesta', 'danger')
                else:
                    flash('Controlla che il valore sia tra lo 0% e il 100% - (Umidita massima)', 'warning')

            if temp_min != plant_s.temperature_min:
                try:
                    snd_req.put(URL_RASPBERRY + '/request', json={'request': 'temp_min', 'serial': idv, 'param': temp_min})
                except:
                    flash('Impossible inoltrare la richiesta', 'danger')

            if temp_max != plant_s.temperature_max:
                try:
                    snd_req.put(URL_RASPBERRY + '/request', json={'request': 'temp_max', 'serial': idv, 'param': temp_max})
                except:
                    flash('Impossible inoltrare la richiesta', 'danger')

            if float(water_container_size) != float(plant_s.water_container_size):
                try:
                    snd_req.put(URL_RASPBERRY + '/request', json={'request': 'water_container_size', 'serial': idv, 'param': water_container_size})
                except:
                    flash('Impossible inoltrare la richiesta', 'danger')

            if send_time != plant_s.send_time:
                if send_time > 1:
                    try:
                        snd_req.put(URL_RASPBERRY + '/request',
                                    json={'request': 'send_time', 'serial': idv, 'param': send_time})
                    except:
                        flash('Impossible inoltrare la richiesta - (Tempo invio dati)', 'error')
                else:
                    flash('Il tempo trascorso deve essere almeno di un minuto! - (Tempo invio dati)', 'danger')

            if int(transmit_power) != int(plant_s.transmit_power):
                try:
                    snd_req.put(URL_RASPBERRY + '/request',
                                json={'request': 'vase_transmit_power', 'serial': idv, 'param': transmit_power})
                    flash('Richiesta inoltrata alla radio (Potenza trasmissione dati)', 'success')
                except:
                    flash('Impossible inoltrare la richiesta - (Potenza trasmissione dati)', 'danger')

            time.sleep(4)
            return redirect('/settings/' + idv)

        else:
            return render_template('plant_settings.html',
                                   connections=conn_list,
                                   typeplant=type_list,
                                   plant=plant_s,
                                   form=settings_form,
                                   title="Settings")