from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class SettingsForm(FlaskForm):
    hum_min = IntegerField('Umidita minima')
    hum_max = IntegerField('Umidita massima')
    temp_min = IntegerField('Temperatura minima')
    temp_max = IntegerField('Temperatura massima')
    light_min = IntegerField('Luce minima')
    light_max = IntegerField('Luce massima')
    submit = SubmitField('Imposta')