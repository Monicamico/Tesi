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
    radio_list = Radio.query.all()
    plants_list = Plant.query.all()
    n_None = 0
    n_2 = 0
    n_4 = 0
    n_6 = 0
    n_8 = 0
    n_10 = 0
    data2 = list()
    for plant in plants_list:
        if plant.state_fitness is None:
            n_None = n_None + 1
        else:
            if 0.0 <= plant.state_fitness < 0.2:
                n_2 = n_2 + 1
            if 0.2 <= plant.state_fitness < 0.4:
                n_4 = n_4 + 1
            if 0.4 <= plant.state_fitness < 0.6:
                n_6 = n_6 + 1
            if 0.6 <= plant.state_fitness < 0.8:
                n_8 = n_8 + 1
            if 0.8 <= plant.state_fitness <= 1.0:
                n_10 = n_10 + 1

    data = [{"n_2": n_2, "n_4": n_4,
             "n_6": n_6, "n_8": n_8,
             "n_10": n_10, "n_None": n_None}]

    for radio in radio_list:
        n_plant = 0
        for plant in plants_list:
            if plant.radio_id == radio.id:
                n_plant = n_plant + 1
        elem = {"radio": radio.name, "num": n_plant}
        data2.append(elem)

    datajson = json.dumps(data)
    datajson2 = json.dumps(data2)
    conn_list = ConnectionRequest.query.all()
    return render_template('dashboard.html',
                           form=form,
                           plants=plants_list,
                           radios=radio_list,
                           connections=conn_list,
                           data=datajson,
                           data2=datajson2)
