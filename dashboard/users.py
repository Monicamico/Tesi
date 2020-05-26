from flask import Blueprint, render_template
from flask_login import login_required
from auth import is_admin
from gio_db import User, ConnectionRequest

users_page = Blueprint('users_page', __name__)


@login_required
@users_page.route('/users')
def users_list_page():
    if is_admin():
        users_list = User.query.all()
        conn_list = ConnectionRequest.query.all()
        return render_template('users.html',
                               users=users_list,
                               connections=conn_list)

