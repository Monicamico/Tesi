from flask import Blueprint, render_template, json
from flask_login import login_required

from forms import LoginForm
from gio_db import Radio, Plant, db, ConnectionRequest
from constant import URL

map_page = Blueprint('map_page', __name__)


@map_page.route('/map')
@login_required
def mappa_page():
    form = LoginForm()
    plants_list = Plant.query.all()
    radio_list = Radio.query.all()
    nodes = list()
    edges = list()

    elem = {'name': 'dashboard', 'type': 'dashboard', 'toshow': 'Gio-Vase'}
    nodes.append(elem)

    for radio in radio_list:
        elem = {'name': radio.id, 'type': 'radio', 'toshow': radio.name}
        nodes.append(elem)
        elem = {'src': radio.id, 'dest': 'dashboard'}
        edges.append(elem)

    for plant in plants_list:
        if plant.state_fitness is None:
            vase_color = 'None'
        else:
            if 0.0 <= plant.state_fitness < 0.2:
                vase_color = '0-20'
            if 0.2 <= plant.state_fitness < 0.4:
                vase_color = '20-40'
            if 0.4 <= plant.state_fitness < 0.6:
                vase_color = '40-60'
            if 0.6 <= plant.state_fitness < 0.8:
                vase_color = '60-80'
            if 0.8 <= plant.state_fitness <= 1.0:
                vase_color = '80-100'

        elem = {'name': plant.id, 'type': 'vase',
                'color': vase_color, 'toshow': plant.name,
                'link': URL + '/plant/' + plant.id}
        nodes.append(elem)
        elem = {'src': plant.id, 'dest': plant.radio_id}
        edges.append(elem)

    data = {
        "nodes": nodes,
        "edges": edges
    }

    datajson = json.dumps(data)
    conn_list = ConnectionRequest.query.all()
    return render_template('map.html', radios= radio_list,form=form, connections=conn_list, data=datajson)
