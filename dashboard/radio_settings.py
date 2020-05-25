import time
from flask import Blueprint, render_template, request as rcv_req, redirect, flash
from flask_login import login_required
from auth import is_admin
from forms import SettingsForm
from gio_db import Radio, url_from_radio, update_radio_name, ConnectionRequest, update_radio_transmit_power
import requests as snd_req

radio_settings_page = Blueprint('radio_settings_page', __name__)


@radio_settings_page.route('/radio_settings/<string:idr>', methods=['POST', 'GET'])
@login_required
def radio_settings(idr):
    radio = Radio.query.filter_by(id=idr).first()
    conn_list = ConnectionRequest.query.all()
    settings_form = SettingsForm()
    if is_admin():
        url_raspberry = str(url_from_radio(idr))
        if url_raspberry is None:
            flash(u'Errore di connessione con la radio','danger')
            return redirect("radio_settings/" + idr)

        if settings_form.validate_on_submit():
            radio_name = rcv_req.form['radio_name']
            transmit_power = int(rcv_req.form.get('transmit_power'))
            sleep_time = int(rcv_req.form['sleep_time'])

            if radio_name != radio.name:
                if update_radio_name(idr, radio_name):
                    flash(u'Nome della radio cambiato con successo','success')
                else:
                    flash(u'Impossibile cambiare il nome della radio','danger')
                    redirect('/radio_settings/' + idr)

            if transmit_power != radio.transmit_power:
                if 0 < transmit_power < 8:
                    try:
                        snd_req.put(url_raspberry + '/request', json={'request': 'radio_transmit_power',
                                                                      'serial': idr,
                                                                      'param': transmit_power})
                        flash(u'Potenza del segnale di trasmissione cambiato con successo', 'success')
                    except:
                        flash(u'Impossibile cambiare la potenza del segnale di trasmissione', 'danger')
                        redirect('/radio_settings/'+idr)
                else:
                    flash(u'Controlla che il valore sia tra 1 e 7', 'warning')
                    redirect('/radio_settings/' + idr)

            if sleep_time != radio.sleep_time:
                if sleep_time > 0:
                    try:
                        snd_req.put(url_raspberry + '/request', json={'request': 'sleep_time',
                                                                      'serial': idr,
                                                                      'param': sleep_time})
                        flash(u'Richiesta inoltrata con successo - Sleep Time', 'success')
                    except:
                        flash(u'Impossibile inoltrare la richiesta alla radio', 'danger')
                        redirect('/radio_settings/' + idr)
                else:
                    flash(u'Il tempo deve essere maggiore di 0', 'warning')
                    redirect('/radio_settings/' + idr)

            return redirect('/radio_settings/'+idr)

        else:
            return render_template('radio_settings.html',
                                   connections=conn_list,
                                   radio=radio,
                                   form=settings_form,
                                   title="Radio Settings")