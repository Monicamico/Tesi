from flask import Blueprint, render_template, request as http_req
from gio_db import Radio, add_radio

radios_page = Blueprint('radios_page',__name__)


@radios_page.route('/radio')
def plants():
    radios_list = Radio.query.all()
    return render_template('radios.html',
                           radio_list=radios_list)
