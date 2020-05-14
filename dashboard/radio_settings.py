from flask import Blueprint, render_template, request as rcv_req, redirect
from forms import SettingsForm
from gio_db import Radio, url_from_radio, update_radio_name, ConnectionRequest

radio_settings_page = Blueprint('radio_settings_page', __name__)


@radio_settings_page.route('/radio_settings/<string:idr>/<string:alert>', methods=['POST', 'GET'])
def radio_settings(idr, alert):
    radio = Radio.query.filter_by(id=idr).first()
    conn_list = ConnectionRequest.query.all()
    settings_form = SettingsForm()

    url_raspberry = str(url_from_radio(idr))
    if url_raspberry is None:
        return render_template('radio_settings.html',
                               alert='fail-url',
                               connections=conn_list,
                               radio=radio,
                               form=settings_form,
                               title="Radio Settings")

    if settings_form.validate_on_submit():
        radio_name = rcv_req.form['radio_name']

        if radio_name != radio.name:
            if update_radio_name(idr, radio_name):
                alert = 'success'
            else:
                alert = 'fail'
        else:
            alert = 'fail-param'

    return render_template('radio_settings.html',
                           alert=alert,
                           connections=conn_list,
                           radio=radio,
                           form=settings_form,
                           title="Radio Settings")