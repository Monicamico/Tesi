from flask import Blueprint, render_template, flash, request as rcv_req, redirect
from flask_login import login_required
from auth import is_admin
from forms import UserForm
from gio_db import ConnectionRequest, add_user

adduser_page = Blueprint('adduser_page', __name__)


@login_required
@adduser_page.route('/add_user', methods=['POST','GET'])
def add_user_page():
    if is_admin():
        form = UserForm()
        conn_list = ConnectionRequest.query.all()
        if form.validate_on_submit():
            try:
                username = rcv_req.form['username']
                if username == '':
                    raise ValueError
            except:
                flash('Inserisci un username', 'warning')
                return redirect('#')
            try:
                password = rcv_req.form['password']
                password_repeat = rcv_req.form['password_repeat']
                if password == '' or password_repeat == '':
                    raise ValueError
            except:
                flash('Inserisci password', 'warning')
                return redirect('#')
            try:
                ruolo_utente = int(rcv_req.form.get('ruolo_utente'))
            except:
                flash('Inserisci un ruolo','warning')
                return redirect('#')

            if password == password_repeat:
                if add_user(username=username, password=password_repeat,role=ruolo_utente):
                    flash(u'Utente registrato con successo','success')
                    return redirect('/users')
                else:
                    flash(u'Impossibile registrare utente','danger')
            else:
                flash(u'Ricontrolla i parametri', 'warning')
            redirect('#')

        return render_template('add_user.html',
                               form=form,
                               connections=conn_list)