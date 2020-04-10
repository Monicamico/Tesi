from gio_db import add_conn_req, delete_conn_req, ConnectionRequest
from flask import Blueprint, render_template, request as http_req


connections_page = Blueprint('connections', __name__)


@connections_page.route("/add_conn_request", methods=['POST', 'PUT'])
def conn_req():
    data = http_req.json
    add_conn_req(data['serial'], data['ping'])
    return 'ok'


@connections_page.route("/delete_conn_request", methods=['POST', 'PUT'])
def del_conn_req():
    data = http_req.json
    delete_conn_req(data['serial'])
    return "ok"


@connections_page.route('/connections')
def conn_page():
    conn_list = ConnectionRequest.query.all()
    return render_template('connections.html',
                           connections=conn_list,
                           title="Gio-Vase")
