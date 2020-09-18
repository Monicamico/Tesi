from flask import Blueprint, render_template, flash, request as rcv_req, redirect
from flask_login import login_required, current_user
from flask_login import login_manager
from view.login import admin
from model.forms import UserForm
from model.gio_db import ConnectionRequest
from controller.utility import correct_password_user, get_user

user_settings_page = Blueprint('user_settings_page', __name__)


@login_required
@user_settings_page.route('/user_settings/<string:user>', methods=['POST', 'GET'])
def user_settings(user):
    """
    If current user is admin, show the user's settings.

    :param user: username
    :type user: str
    :return: template *user_settings.html* or *error.html*
    :rtype: template
    """

    if current_user.username == user or admin():
        form = UserForm()
        conn_list = ConnectionRequest.query.all()
        user_first = get_user(user)

        if form.validate_on_submit():
            try:
                username = rcv_req.form['username']
                if username == '':
                    raise ValueError
            except:
                flash('Inserisci un username', 'warning')

            try:
                password = rcv_req.form['password']
                if password == '':
                    raise ValueError
            except:
                flash('Inserisci la password', 'warning')

            try:
                new_password = rcv_req.form['new_password']
                password_repeat = rcv_req.form['password_repeat']
            except:
                print('password non cambiata')

            try:
                ruolo_utente = int(rcv_req.form.get('ruolo_utente'))
            except:
                flash('Inserisci un ruolo', 'warning')

            if correct_password_user(user_first.username, password) is True:

                if new_password is not None and password_repeat is not None:
                    if new_password == password_repeat != '':
                        user_first.set_password(new_password)
                        flash('Password cambiata con successo', 'success')
                    else:
                        if new_password != password_repeat and new_password != '' and password_repeat != '':
                            flash('Password non corrispondenti', 'danger')

                if user_first.username != username:
                    if user_first.set_username(username) is True:
                        flash('Username cambiato con successo', 'success')

                if user_first.role != ruolo_utente:
                    try:
                        if ruolo_utente != 1 and ruolo_utente != 0:
                            raise ValueError
                        user_first.set_role(ruolo_utente)
                        flash('Ruolo cambiato con successo','success')
                    except:
                        flash('Ruolo errato', 'warning')
            else:
                flash('Per apportare modifiche al profilo inserisci la password', 'danger')

            redirect('#')
        return render_template('user_settings.html',
                               form=form,
                               user=user_first,
                               connections=conn_list)
    else:
        return login_manager.unauthorized()