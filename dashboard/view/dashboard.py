from flask import Blueprint, render_template, request as http_req
from flask import json
from flask_login import login_required

from forms import LoginForm
from gio_db import ConnectionRequest, Plant, Radio

dashboard_page = Blueprint('dashboard_page', __name__)


@dashboard_page.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dash_page():

    form = LoginForm()
    conn_list = ConnectionRequest.query.all()
    radio_list = Radio.query.all()
    plants_list = Plant.query.all()
    nodes = list()
    edges = list()
    n_None = 0
    n_2 = 0
    n_4 = 0
    n_6 = 0
    n_8 = 0
    n_10 = 0
    data2 = list()
    elem = {'name': 'dashboard', 'type': 'dashboard', 'toshow': 'Gio-Vase'}
    nodes.append(elem)

    for plant in plants_list:
        if plant.state_fitness is None:
            vase_color = 'None'
            n_None = n_None + 1
        else:
            if 0.0 <= plant.state_fitness < 0.2:
                vase_color = '0-20'
                n_2 = n_2 + 1
            if 0.2 <= plant.state_fitness < 0.4:
                vase_color = '20-40'
                n_4 = n_4 + 1
            if 0.4 <= plant.state_fitness < 0.6:
                vase_color = '40-60'
                n_6 = n_6 + 1
            if 0.6 <= plant.state_fitness < 0.8:
                vase_color = '60-80'
                n_8 = n_8 + 1
            if 0.8 <= plant.state_fitness <= 1.0:
                vase_color = '80-100'
                n_10 = n_10 + 1

        elem = {'name': plant.id, 'type': 'vase',
                'color': vase_color, 'toshow': plant.name,
                'link': '/plant/' + plant.id}
        nodes.append(elem)
        elem = {'src': plant.id, 'dest': plant.radio_id}
        edges.append(elem)

    data = [{"n_2": n_2, "n_4": n_4,
             "n_6": n_6, "n_8": n_8,
             "n_10": n_10, "n_None": n_None}]

    for radio in radio_list:
        elem = {'name': radio.id, 'type': 'radio', 'toshow': radio.name}
        nodes.append(elem)
        elem = {'src': radio.id, 'dest': 'dashboard'}
        edges.append(elem)

        n_plant = 0
        for plant in plants_list:
            if plant.radio_id == radio.id:
                n_plant = n_plant + 1
        element = {"radio": radio.name, "num": n_plant}
        data2.append(element)

    data3 = {
        "nodes": nodes,
        "edges": edges
    }

    datajson3 = json.dumps(data3)
    datajson = json.dumps(data)
    datajson2 = json.dumps(data2)

    return render_template('dashboard.html',
                           form=form,
                           plants=plants_list,
                           radios=radio_list,
                           connections=conn_list,
                           data=datajson,
                           data2=datajson2,
                           data3=datajson3)
