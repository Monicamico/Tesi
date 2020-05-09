from flask import Blueprint, render_template, request as http_req
from flask import json
from gio_db import ConnectionRequest, Plant

homepage = Blueprint('homepage', __name__)


@homepage.route('/')
def layout_page():
    conn_list = ConnectionRequest.query.all()
    return render_template('home.html',
                           connections=conn_list)


@homepage.route('/home')
def home_page():
    conn_list = ConnectionRequest.query.all()
    return render_template('home.html',
                           connections=conn_list)


@homepage.route('/dashboard')
def dash_page():
    plants_list = Plant.query.all()
    n_sad = 0
    n_happy = 0
    for plant in plants_list:
        if not plant.state:
            n_sad = n_sad + 1
        else:
            n_happy = n_happy + 1
    data = [{"happy": n_happy, "sad": n_sad}]
    datajson = json.dumps(data)
    return render_template('dashboard.html',data=datajson)
