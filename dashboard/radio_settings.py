from flask import Blueprint, render_template, request as rcv_req, redirect
from forms import SettingsForm
from constant import URL
import requests as snd_req

from gio_db import Radio, url_from_radio, update_radio_name, ConnectionRequest

radio_settings_page = Blueprint('radio_settings_page', __name__)


@radio_settings_page.route('/radio_settings/<string:idr>', methods=['POST', 'GET'])
def radio_settings(idr):
    radio = Radio.query.filter_by(id=idr).first()
    conn_list = ConnectionRequest.query.all()
    settings_form = SettingsForm()

    url_raspberry = str(url_from_radio(idr))
    if url_raspberry is None:
        return redirect(URL + '/radio_settings/' + str(idr))

    if settings_form.validate_on_submit():
        radio_name = rcv_req.form['radio_name']

        if radio_name != radio.name:
            update_radio_name(idr, radio_name)

    return render_template('radio_settings.html',
                           connections=conn_list,
                           radio=radio,
                           form=settings_form,
                           title="Radio Settings")