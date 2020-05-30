from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired


class SettingsForm(FlaskForm):
    hum_min = IntegerField('Umidita minima:')
    hum_max = IntegerField('Umidita massima:')
    temp_min = IntegerField('Temperatura minima:')
    temp_max = IntegerField('Temperatura massima:')
    light_min = IntegerField('Luce minima:')
    light_max = IntegerField('Luce massima:')
    watering_light = IntegerField('Luce per innaffiare:')
    water_container_size = FloatField('Dimensione contenitore:')
    name = StringField('Nome:')
    radio_name = StringField('Nome radio: ')
    transmit_power = IntegerField('Transmit Power: ')
    sleep_time = IntegerField('Sleep time: ')
    send_time = IntegerField('Send time: ')
    submit = SubmitField('Imposta')


class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Login')


class PlantForm(FlaskForm):
    name = StringField('Nome pianta')
    submit = SubmitField('Conferma')


class UserForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    password_repeat = PasswordField('Ripeti password')
    new_password = PasswordField('Nuova password')
    ruolo_utente = StringField('Ruolo')
    submit = SubmitField('Registra')
