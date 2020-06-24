from flask import Blueprint, render_template
from flask_login import login_required

from model.gio_db import Plant, Radio, ConnectionRequest

plants_page = Blueprint('plants_page',__name__)


@plants_page.route('/plants')
@login_required
def plants():
    plants_list = Plant.query.all()
    radios_list = Radio.query.all()
    conn_list = ConnectionRequest.query.all()
    return render_template('plants.html',
                           plants=plants_list,
                           radios=radios_list,
                           connections=conn_list,
                           searchBar = 'si',
                           title='Plants List')



