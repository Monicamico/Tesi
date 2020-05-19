from flask import Blueprint, render_template, request as http_req
from gio_db import Plant, add_plant, delete_plant, Radio, ConnectionRequest

plants_page = Blueprint('plants_page',__name__)


@plants_page.route('/plants/<string:alert>')
def plants_alert(alert):
    plants_list = Plant.query.all()
    radios_list = Radio.query.all()
    conn_list = ConnectionRequest.query.all()
    return render_template('plants.html',
                           alert=alert,
                           plants=plants_list,
                           radios=radios_list,
                           connections=conn_list,
                           searchBar = 'si',
                           title='Plants List')



