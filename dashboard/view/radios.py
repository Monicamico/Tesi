from flask import Blueprint, render_template, request as http_req
from flask_login import login_required

from auth import is_admin
from gio_db import Radio, ConnectionRequest

radios_page = Blueprint('radios_page',__name__)


@radios_page.route('/radios')
@login_required
def radios():
    if is_admin():
        radios_list = Radio.query.all()
        conn_list = ConnectionRequest.query.all()
        return render_template('radios.html',
                               connections=conn_list,
                               radio_list=radios_list)

