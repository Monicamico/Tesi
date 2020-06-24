from flask_login import login_manager, current_user, LoginManager, login_required, logout_user, login_user
from model.gio_db import User, get_user
from flask import Blueprint, redirect, flash, render_template, request as rcv_req
from model.forms import LoginForm

login_manager = LoginManager()

auth = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


def is_admin():
    if current_user.is_authenticated and current_user.is_admin:
        return True
    else:
        return login_manager.unauthorized()


@auth.route('/login', methods=['GET', 'POST'])
def login():

    if hasattr(current_user, "is_authenticated") and current_user.is_authenticated:
        return redirect("/home")

    form = LoginForm()
    if form.validate_on_submit():
        name = rcv_req.form['username']
        pwd = rcv_req.form['password']
        user = get_user(name)
        if user is not None and user.authenticate(password=pwd):
            if login_user(user):
                flash('Login effettuato con succeesso','success')
                return redirect('/home')
            else:
                flash("Impossibile effettuare il login",'error')
                return redirect('/login')
        else:
            flash("Username o password errati")
            return redirect("/login")
    return render_template('login.html', form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/login')