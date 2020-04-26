from flask import Blueprint, render_template, request as http_req
from gio_db import Plant, add_plant, delete_plant


plants_page = Blueprint('plants_page',__name__)


@plants_page.route("/add_plant", methods=['POST', 'PUT'])
def add_plant_id():
    data = http_req.json
    add_plant(data['serial'], data['ping'], data['radio_serial'])
    return "ok"


@plants_page.route("/delete_plant", methods=['POST', 'PUT'])
def delete_plant_id():
    data = http_req.json
    delete_plant(data['serial'])
    return "ok"


@plants_page.route('/plants')
def plants():
    plants_list = Plant.query.all()
    return render_template('plants.html',
                           plants=plants_list,
                           title='Plants List')
