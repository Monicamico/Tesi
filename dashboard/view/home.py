from flask import Blueprint, render_template
from model.gio_db import ConnectionRequest

homepage = Blueprint('homepage', __name__)


@homepage.route('/', methods=['GET', 'POST'])
def layout_page():
    conn_list = ConnectionRequest.query.all()
    return render_template('home.html',
                           connections=conn_list)


@homepage.route('/home', methods=['GET', 'POST'])
def home_page():
    conn_list = ConnectionRequest.query.all()
    return render_template('home.html',
                           connections=conn_list)


@homepage.app_errorhandler(404)
def not_found_page(error):
    return render_template('error.html', error='404')


@homepage.app_errorhandler(401)
def permission_denied_page(error):
    return render_template('error.html', error='401')

