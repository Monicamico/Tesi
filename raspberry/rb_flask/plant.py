from flask import Blueprint, render_template, request as http_req

plant = Blueprint('plant', __name__)



@plant.route("/water", methods=['POST', 'PUT'])
def water():
    data = http_req.json
