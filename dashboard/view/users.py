from flask import Blueprint, render_template
from flask_login import login_required
from view.login import is_admin
from model.gio_db import User, ConnectionRequest

users_page = Blueprint('users_page', __name__)


@login_required
@users_page.route('/users')
def users_list_page():
    """

    If current user is admin, show all the users.

    :return: template *users.html*
    :rtype: template

    """
    if is_admin():
        users_list = User.query.all()
        conn_list = ConnectionRequest.query.all()
        return render_template('users.html',
                               users=users_list,
                               connections=conn_list)

