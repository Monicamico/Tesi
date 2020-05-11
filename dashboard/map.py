from flask import Blueprint, render_template, json
from gio_db import Radio, Plant, db, ConnectionRequest

map_page = Blueprint('map_page', __name__)


@map_page.route('/map')
def dash_page():
    plants_list = Plant.query.all()
    radio_list = Radio.query.all()
    nodes = list()
    edges = list()

    elem = {'name': 'dashboard', 'type': 'dashboard', 'toshow': 'Dip. di Informatica'}
    nodes.append(elem)

    for radio in radio_list:
        elem = {'name': radio.id, 'type': 'radio', 'toshow': radio.name}
        nodes.append(elem)
        elem = {'src': radio.id, 'dest': 'dashboard'}
        edges.append(elem)

    for plant in plants_list:
        if plant.state is False:
            elem = {'name': plant.id, 'type': 'vase', 'color': 'sad', 'toshow': plant.name}
        else:
            elem = {'name': plant.id, 'type': 'vase', 'color': 'happy', 'toshow': plant.name}
        nodes.append(elem)
        elem = {'src': plant.id, 'dest': plant.radio_id}
        edges.append(elem)

    data = {
        "nodes": nodes,
        "edges": edges
    }

    datajson = json.dumps(data)
    conn_list = ConnectionRequest.query.all()
    return render_template('map.html', connections=conn_list, data=datajson)
