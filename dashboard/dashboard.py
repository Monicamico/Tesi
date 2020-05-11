from flask import Blueprint, render_template, request as http_req
from flask import json
from gio_db import ConnectionRequest, Plant, Radio

dashboard_page = Blueprint('dashboard_page', __name__)


@dashboard_page.route('/dashboard')
def dash_page():
    radio_list = Radio.query.all()
    plants_list = Plant.query.all()
    n_sad = 0
    n_happy = 0
    data2 = list()
    for plant in plants_list:
        if not plant.state:
            n_sad = n_sad + 1
        else:
            n_happy = n_happy + 1
    data = [{"happy": n_happy, "sad": n_sad}]

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
                           plants=plants_list,
                           radios=radio_list,
                           connections=conn_list,
                           data=datajson,
                           data2=datajson2)
