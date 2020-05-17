import sqlite3
from math import ceil

import sqlalchemy
from flask import Blueprint, render_template, request as rcv_req, redirect
from forms import SettingsForm
from gio_db import Plant, update_name, url_from_plant, ConnectionRequest
import time
import requests as snd_req

settings_page = Blueprint('settings_page', __name__)


@settings_page.route('/settings/<string:idv>/<string:alert>', methods=['POST', 'GET'])
def settings(idv, alert):
    plant_s = Plant.query.filter_by(id=idv).first()
    conn_list = ConnectionRequest.query.all()
    settings_form = SettingsForm()
    URL_RASPBERRY = str(url_from_plant(idv))
    if URL_RASPBERRY == str(-1):
        return redirect("settings/" + idv + "/" + "url-fail")

    if settings_form.validate_on_submit():
        name = rcv_req.form['name']
        light_max = ceil(int(rcv_req.form['light_max']) / 100 * 255)
        light_min = ceil(int(rcv_req.form['light_min']) / 100 * 255)
        temp_max = int(rcv_req.form['temp_max'])
        temp_min = int(rcv_req.form['temp_min'])
        hum_min = ceil(int(rcv_req.form['hum_min']) / 100 * 1023)
        hum_max = ceil(int(rcv_req.form['hum_max']) / 100 * 1023)
        watering_light = ceil(int(rcv_req.form['watering_light']) / 100 * 255)
        water_container_size = rcv_req.form['water_container_size']
        transmit_power = int(rcv_req.form.get('transmit_power'))
        send_time = int(rcv_req.form.get('send_time'))
        alert = 'success'

        if name != plant_s.name:
            if update_name(idv, name):
                return redirect("name_success")
            else:
                return redirect("name_fail")

        if light_max != plant_s.light_max:
            if 0 <= light_max <= 255 and alert == 'success':
                try:
                    snd_req.put(URL_RASPBERRY + '/request', json=dict(request='light_max', serial=idv, param=light_max))
                except:
                    alert = 'fail'
            else:
                alert = 'param-fail'

        if light_min != plant_s.light_min:
            if 0 <= light_min <= 255 and alert == 'success':
                try:
                    snd_req.put(URL_RASPBERRY + '/request',
                                json={'request': 'light_min', 'serial': idv, 'param': light_min})
                except:
                    alert = 'fail'
            else:
                alert = 'param-fail'

        if watering_light != plant_s.watering_light:
            if 0 <= watering_light <= 255 and alert == 'success':
                try:
                    snd_req.put(URL_RASPBERRY + '/request',
                                json={'request': 'watering_light', 'serial': idv, 'param': watering_light})
                except:
                    alert = 'fail'
            else:
                alert = 'param-fail'

        if hum_min != plant_s.humidity_min:
            if 0 <= hum_min <= 1023  and alert == 'success':
                try:
                    snd_req.put(URL_RASPBERRY + '/request', json={'request': 'hum_min', 'serial': idv, 'param': hum_min})
                except:
                    alert = 'fail'
            else:
                alert = 'param-fail'

        if hum_max != plant_s.humidity_max:
            if 0 <= hum_max <= 1023 and alert == 'success':
                try:
                    snd_req.put(URL_RASPBERRY + '/request', json={'request': 'hum_max', 'serial': idv, 'param': hum_max})
                except:
                    alert = 'fail'
            else:
                alert = 'param-fail'

        if temp_min != plant_s.temperature_min:
            if alert == 'success':
                try:
                    snd_req.put(URL_RASPBERRY + '/request', json={'request': 'temp_min', 'serial': idv, 'param': temp_min})
                except:
                    alert = 'fail'

        if temp_max != plant_s.temperature_max and alert == 'success':
            try:
                snd_req.put(URL_RASPBERRY + '/request', json={'request': 'temp_max', 'serial': idv, 'param': temp_max})
                alert = 'success'
            except:
                alert = 'fail'

        if float(water_container_size) != float(plant_s.water_container_size) and alert == 'success':
            try:
                snd_req.put(URL_RASPBERRY + '/request', json={'request': 'water_container_size', 'serial': idv, 'param': water_container_size})
                alert = 'success'
            except:
                alert = 'fail'

        if send_time != plant_s.send_time:
            if send_time > 1 and alert == 'success':
                try:
                    snd_req.put(URL_RASPBERRY + '/request',
                                json={'request': 'send_time', 'serial': idv, 'param': send_time})
                    alert = 'success'
                except:
                    alert = 'fail'
            else:
                alert = 'param-fail'

        if int(transmit_power) != int(plant_s.transmit_power):
            if alert == 'success':
                try:
                    snd_req.put(URL_RASPBERRY + '/request',
                                json={'request': 'vase_transmit_power', 'serial': idv, 'param': transmit_power})
                    alert = 'success'
                except:
                    alert = 'fail'

        if alert == 'success':
            time.sleep(5)

        return redirect(alert)

    else:
        return render_template('plant_settings.html',
                               alert=alert,
                               connections=conn_list,
                               plant=plant_s,
                               form=settings_form,
                               title="Settings")
