from flask import Blueprint, render_template, request as http_req
from gio_db import ConnectionRequest

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
    conn_list = ConnectionRequest.query.all()
    return render_template('dashboard.html',
                           connections=conn_list)
