from flask import Blueprint, render_template, request as rcv_req, redirect
from forms import SettingsForm
from gio_db import Plant

from constant import URL_RASPBERRY, URL
import requests as snd_req


settings_page = Blueprint('settings_page', __name__)


@settings_page.route('/settings/<string:idv>', methods=['POST', 'GET'])
def settings(idv):
    plant_s = Plant.query.filter_by(id=idv).first()
    settings_form = SettingsForm()
    if settings_form.validate_on_submit():
        pass
    return render_template('settings.html',
                           plant=plant_s,
                           form=settings_form,
                           title="Settings")