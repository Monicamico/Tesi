import time
from flask import Blueprint, render_template, request as rcv_req, redirect
from forms import SettingsForm
from gio_db import Radio, url_from_radio, update_radio_name, ConnectionRequest, update_radio_transmit_power
import requests as snd_req

radio_settings_page = Blueprint('radio_settings_page', __name__)


@radio_settings_page.route('/radio_settings/<string:idr>/<string:alert>', methods=['POST', 'GET'])
def radio_settings(idr, alert):
    radio = Radio.query.filter_by(id=idr).first()
    conn_list = ConnectionRequest.query.all()
    settings_form = SettingsForm()

    url_raspberry = str(url_from_radio(idr))
    if url_raspberry is None:
        return redirect("radio_settings/" + idr + "/" + "url-fail")

    if settings_form.validate_on_submit():
        radio_name = rcv_req.form['radio_name']
        transmit_power = int(rcv_req.form['transmit_power'])
        sleep_time = int(rcv_req.form['sleep_time'])

        if radio_name != radio.name:
            if update_radio_name(idr, radio_name):
                alert = 'success'
            else:
                alert = 'fail'

        if transmit_power != radio.transmit_power:
            if 0 < transmit_power < 8:
                try:
                    snd_req.put(url_raspberry + '/request', json={'request': 'radio_transmit_power',
                                                                  'serial': idr,
                                                                  'param': transmit_power})
                    alert = 'success'
                except:
                    alert = 'fail'
            else:
                alert = 'param-fail'

        if sleep_time != radio.sleep_time:
            if sleep_time > 0:
                alert = 'success'
            else:
                alert = 'param-fail'

        if alert == 'success':
            time.sleep(2)

        return redirect(alert)

    else:
        return render_template('radio_settings.html',
                               alert=alert,
                               connections=conn_list,
                               radio=radio,
                               form=settings_form,
                               title="Radio Settings")