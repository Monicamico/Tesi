from flask import Blueprint, render_template, request as http_req
from gio_db import add_conn_req, delete_conn_req, add_plant, delete_plant

homepage = Blueprint('homepage', __name__)


@homepage.route("/conn_request", methods=['POST', 'PUT'])
def conn_req():
    data = http_req.json
    add_conn_req(data['serial'])
    return 'ok'


@homepage.route("/delete_conn_request", methods=['POST', 'PUT'])
def del_conn_req():
    data = http_req.json
    delete_conn_req(data['serial'])
    return "ok"


@homepage.route("/add_plant", methods=['POST', 'PUT'])
def add_plant_id():
    data = http_req.json
    add_plant(data['serial'], data['ping'])
    return "ok"


@homepage.route("/delete_plant", methods=['POST', 'PUT'])
def delete_plant_id():
    data = http_req.json
    delete_plant(data['serial'])
    return "ok"

@homepage.route("/home")
def home_page():
    return render_template('home.html', title="Gio-Vase")
