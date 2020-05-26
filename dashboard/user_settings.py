from flask import Blueprint, render_template, flash, request as rcv_req, redirect
from flask_login import login_required
from auth import is_admin
from forms import UserForm
from gio_db import ConnectionRequest, add_user, User

user_settings_page = Blueprint('user_settings_page', __name__)


@login_required
@user_settings_page.route('/user_settings/<string:user>', methods=['POST','GET'])
def user_settings(user):
    if is_admin():
        conn_list = ConnectionRequest.query.all()
        user_first = User.query.filter_by(username=user).first()
        return render_template('user_settings.html',
                               user=user_first,
                               connections=conn_list)