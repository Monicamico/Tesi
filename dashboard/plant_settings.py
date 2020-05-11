from math import ceil
from flask import Blueprint, render_template, request as rcv_req, redirect
from forms import SettingsForm
from gio_db import Plant, update_name, url_from_plant
import time
from constant import URL
import requests as snd_req

settings_page = Blueprint('settings_page', __name__)


@settings_page.route('/settings/<string:idv>', methods=['POST', 'GET'])
def settings(idv):
    plant_s = Plant.query.filter_by(id=idv).first()
    settings_form = SettingsForm()
    URL_RASPBERRY = str(url_from_plant(idv))
    if URL_RASPBERRY == str(-1):
        return redirect(URL + '/settings/' + str(idv))

    if settings_form.validate_on_submit():
        name = rcv_req.form['name']
        light_max = ceil(int(rcv_req.form['light_max']) / 100 * 255)
        light_min = ceil(int(rcv_req.form['light_min']) / 100 * 255)
        temp_max = int(rcv_req.form['temp_max'])
        temp_min = int(rcv_req.form['temp_min'])
        hum_min = ceil(int(rcv_req.form['hum_min']) / 100 * 1023)
        hum_max = ceil(int(rcv_req.form['hum_max']) / 100 * 1023)
        watering_light = ceil(int(rcv_req.form['watering_light']) / 100 * 255)

        if name != plant_s.name:
            update_name(idv, name)

        if light_max != plant_s.light_max:
            try:
                snd_req.put(URL_RASPBERRY + '/request', json=dict(request='light_max', serial=idv, param=light_max))
            except:
                print('impossibile inoltrare la richiesta')

        if light_min != plant_s.light_min:
            try:
                snd_req.put(URL_RASPBERRY + '/request', json={'request': 'light_min', 'serial': idv, 'param': light_min})
            except:
                print('impossibile inoltrare la richiesta')

        if watering_light != plant_s.watering_light:
            try:
                snd_req.put(URL_RASPBERRY + '/request', json={'request': 'watering_light', 'serial': idv, 'param': watering_light})
            except:
                print('impossibile inoltrare la richiesta')

        if hum_min != plant_s.humidity_min:
            try:
                snd_req.put(URL_RASPBERRY + '/request', json={'request': 'hum_min', 'serial': idv, 'param': hum_min})
            except:
                print('impossibile inoltrare la richiesta')

        if hum_max != plant_s.humidity_max:
            try:
                snd_req.put(URL_RASPBERRY + '/request', json={'request': 'hum_max', 'serial': idv, 'param': hum_max})
            except:
                print('impossibile inoltrare la richiesta')

        if temp_min != plant_s.temperature_min:
            try:
                snd_req.put(URL_RASPBERRY + '/request', json={'request': 'temp_min', 'serial': idv, 'param': temp_min})
            except:
                print('impossibile inoltrare la richiesta')

        if temp_max != plant_s.temperature_max:
            try:
                snd_req.put(URL_RASPBERRY + '/request', json={'request': 'temp_max', 'serial': idv, 'param': temp_max})
            except:
                print('impossibile inoltrare la richiesta')

        time.sleep(4)
        return redirect(URL + '/settings/' + str(idv))

    return render_template('plant_settings.html',
                           plant=plant_s,
                           form=settings_form,
                           title="Settings")
