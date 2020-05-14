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
    water_container_size = FloatField('Dimensione contenitore (litri):')
    name = StringField('Nome:')
    radio_name = StringField('Nome della radio: ')
    submit = SubmitField('Imposta')