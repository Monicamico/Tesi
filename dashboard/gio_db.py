from math import ceil
from time import strftime

from flask_sqlalchemy import SQLAlchemy
import requests as snd_req
from werkzeug.security import generate_password_hash, check_password_hash
from constant import Role
import time

db = SQLAlchemy()


class User(db.Model):
    """
       A class used to represent an User

       Attributes
       ----------
       id : int
          id of the user
       username : str
           the name of the user
       password : str
       role : int
           the role of the User
           0 = Admin
           1 = User

       Methods
       -------
       is_authenticated()
           return the value of the variable is_authenticated

       set_password(password)
           generate a password to authenticate the user

       authenticate(password)
           if the password is correct, it authenticate the user

       get_id()
           returns the id of the user

       set_username(new)
            change the username with new
       """
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)
    role = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)
    is_anonymous = False

    def __init__(self, *args, **kw):
        super(User, self).__init__(*args, **kw)
        self.is_authenticated = False

    def is_authenticated(self):
        return self.is_authenticated

    def set_password(self, password):
        self.password = generate_password_hash(password)
        db.session.commit()

    @property
    def is_admin(self):
        if self.role == Role.ADMIN.value:
            return True
        else:
            return False

    def authenticate(self, password):
        # print(password, " ", self.password)
        checked = check_password_hash(self.password, password)
        self.is_authenticated = checked
        return self.is_authenticated

    def get_id(self):
        return self.id

    def set_username(self,username):
        try:
            self.username = username
            db.session.commit()
            return True
        except:
            return False

    def set_role(self,role):
        self.role = role
        db.session.commit()
        return True


def correct_password_user(username, password):
    """ :return true if the password is correct otherwise false"""
    user = User.query.filter_by(username=username).first()
    checked = check_password_hash(user.password, password)
    return checked


def get_user(username):
    """ :return the user with username equal to the parameter, if it exist, otherwise none. """
    user = User.query.filter_by(username=username).first()
    return user


def add_user(username, password, role):
    """ Add a user into the database

        :param username
        :param password
        :param role

    """
    user = User()
    user.username = username
    user.role = role
    user.set_password(password=password)
    try:
        db.session.add(user)
        db.session.commit()
    except:
        return False
    return True


def delete_user(username, password):
    user = get_user(username)
    if user:
        if user.authenticate(password=password):
            db.session.delete(user)
            db.session.commit()
            return True
        else:
            return False
    else:
        return False


class ConnectionRequest(db.Model):
    __tablename__ = 'connectionRequest'
    id = db.Column(db.String, primary_key=True, nullable=False)
    # the value of the signal ranges from -128 to -42
    # (-128 means a weak signal and -42 means a strong one.)
    signal = db.Column(db.Integer)
    pairing = db.Column(db.Integer)
    radio_id = db.Column(db.String, primary_key=True)


def add_conn_req(idv, signalv, pairingv, radio_id):
    plant = Plant.query.filter_by(id=idv).first()
    if plant is None:
        conn = ConnectionRequest.query.filter_by(id=idv).first()
        if conn is None:
            db.session.add(ConnectionRequest(id=idv, signal=signalv, pairing=pairingv, radio_id=radio_id))
            db.session.commit()
            return True
        else:
            if int(signalv) > int(conn.signal):
                conn.signal = int(signalv)
                url = 'http://' + url_from_radio(conn.radio_id)
                if conn.radio_id != radio_id:
                    snd_req.put(url + '/request', json={'request': 'refused', 'serial': idv})
                conn.radio_id = radio_id
                db.session.commit()
            conn.pairing = pairingv
            db.session.commit()
    else:
        try:
            snd_req.put('http://' + url_from_plant(idv) + '/request', json={'request': 'joined', 'serial': idv})
        except:
            delete_plant(idv)
            db.session.add(ConnectionRequest(id=idv, signal=signalv, pairing=pairingv, radio_id=radio_id))
            db.session.commit()


def delete_conn_req(idv, radio):
    req = ConnectionRequest.query.filter_by(id=idv, radio_id=radio).first()
    if req is None:
        return None
    db.session.delete(req)
    db.session.commit()
    return req


class Radio(db.Model):
    __tablename__ = 'radio'
    id = db.Column(db.String(13), primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(24), unique=True)
    url_radio = db.Column(db.String(), nullable=False)
    transmit_power = db.Column(db.Integer(), default=7)
    sleep_time = db.Column(db.Integer(), default=10)


def update_radio_name(radio, name):
    r = Radio.query.filter_by(name=name).first()
    if r is None:
        r = Radio.query.filter_by(id=radio).first()
        if r is not None:
            r.name = name
            db.session.commit()
            return True
    return False


def update_sleep_time(radio, time):
    r = Radio.query.filter_by(id=radio).first()
    if r is not None:
        r.sleep_time = time
        db.session.commit()
        return True
    return False


def update_radio_transmit_power(radio, tr):
    r = Radio.query.filter_by(id=radio).first()
    if r is not None:
        r.transmit_power = tr
        db.session.commit()
        return True
    return False


def delete_radio(radio):
    r = Radio.query.filter_by(id=radio).first()
    if r is not None:
        db.session.delete(r)
        db.session.commit()


def add_radio(radio, url_radio):
    r = Radio.query.filter_by(id=radio, url_radio=url_radio).first()
    if r is None:
        r = Radio.query.filter_by(id=radio).first()
        if r is None:
            db.session.add(Radio(id=radio, name=radio,
                                 url_radio=url_radio,
                                 transmit_power=7,
                                 sleep_time=10))
            db.session.commit()
            return True
        # the url of the radio is changed
        else:
            r.url_radio = url_radio
            r.transmit_power = 7
            r.sleep_time = 10
            db.session.commit()
            return False
    else:
        return False


def url_from_radio(radio):
    r = Radio.query.filter_by(id=radio).first()
    if r is not None:
        return r.url_radio
    else:
        return None


def radio_from_url(url):
    r = Radio.query.filter_by(url_radio=url).first()
    return r


def associated_plants(radio_id):
    plants = Plant.query.filter_by(radio_id=radio_id).all()
    return plants


class Plant(db.Model):
    __tablename__ = 'plant'
    id = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    radio_id = db.Column(db.String(13), nullable=False)
    name = db.Column(db.String(24), unique=True)
    state_fitness = db.Column(db.Float)
    humidity = db.Column(db.Integer)
    temperature = db.Column(db.Integer)
    light = db.Column(db.Integer)
    humidity_min = db.Column(db.Integer)
    humidity_max = db.Column(db.Integer)
    temperature_max = db.Column(db.Integer)
    temperature_min = db.Column(db.Integer)
    light_max = db.Column(db.Integer)
    light_min = db.Column(db.Integer)
    watering_light = db.Column(db.Integer, default=70)
    water_container_state = db.Column(db.Boolean, nullable=False, default=True)
    water_container_size = db.Column(db.Float, nullable=False, default=0.5)
    transmit_power = db.Column(db.Integer(), default=7)
    send_time = db.Column(db.Integer(), default=16)


def add_plant(idv, radio):
    print('add_plant')
    r = Radio.query.filter_by(id=radio).first()
    if r is not None:
        plant = Plant.query.filter_by(id=idv).first()
        if plant is None:
            db.session.add(Plant(id=idv,
                                 radio_id=radio,
                                 name=idv,
                                 state_fitness=None,
                                 humidity_min=300,
                                 humidity_max=1000,
                                 temperature_max=30,
                                 temperature_min=15,
                                 light_max=250,
                                 light_min=50,
                                 watering_light=70,
                                 water_container_size=0.5,
                                 water_container_state=True,
                                 transmit_power=5,
                                 send_time=15))
            db.session.commit()
            delete_conn_req(idv, radio)


def url_from_plant(idv):
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        radio = Radio.query.filter_by(id=plant.radio_id).first()
        if radio is not None:
            return 'http://' + radio.url_radio
    return -1


def delete_plant(idv):
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        db.session.delete(plant)
        db.session.commit()


def update_name(idv, name):
    plant = Plant.query.filter_by(name=name).first()
    if plant is None:
        plant = Plant.query.filter_by(id=idv).first()
        if plant is not None:
            plant.name = name
            db.session.commit()
            return True
    return False


def update_vase_transmit_power(idv, tr):
    p = Plant.query.filter_by(id=idv).first()
    if p is not None:
        p.transmit_power = tr
        db.session.commit()


def update_send_time(idv, st):
    p = Plant.query.filter_by(id=idv).first()
    if p is not None:
        p.send_time = st
        db.session.commit()


def update_hum(idv, humidity):
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        plant.humidity = humidity
        update_plant_state_fitness(idv)
        db.session.commit()


def update_temp(idv, temperature):
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        plant.temperature = temperature
        update_plant_state_fitness(idv)
        db.session.commit()


def update_light(idv, light):
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        plant.light = light
        update_plant_state_fitness(idv)
        db.session.commit()


def update_plant_state_fitness(idv):
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        if (plant.humidity is not None) and (plant.temperature is not None) and (plant.light is not None):
            ideal_humidity: int = ceil((plant.humidity_max + plant.humidity_min) / 2)
            hum = abs(int(plant.humidity) - ideal_humidity) / ideal_humidity
            ideal_temperature: int = ceil((plant.temperature_max + plant.temperature_min) / 2)
            temp = abs(plant.temperature - ideal_temperature) / ideal_temperature
            ideal_light: int = ceil((plant.light_max + plant.light_min) / 2)
            lig = abs(int(plant.light) - ideal_light) / ideal_light
            state_fitness = (hum + temp + lig) * 0.33
            state_fitness = round(state_fitness, 2)
            plant.state_fitness = 1 - state_fitness
            db.session.commit()
            print(round(plant.state_fitness, 2))
            return state_fitness
        return None
    return None


def update_temp_min(idv, temp_m):
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        plant.temperature_min = temp_m
        db.session.commit()


def update_temp_max(idv, temp_m):
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        plant.temperature_max = temp_m
        db.session.commit()


def update_hum_min(idv, hum_m):
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        plant.humidity_min = hum_m
        db.session.commit()


def update_hum_max(idv, hum_m):
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        plant.humidity_max = hum_m
        db.session.commit()


def update_light_max(idv, li_m):
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        plant.light_max = li_m
        db.session.commit()


def update_light_min(idv, li_m):
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        plant.light_min = li_m
        db.session.commit()


def update_watering_light(idv, wl):
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        plant.watering_light = wl
        db.session.commit()


def update_water_container_size(idv, wcs):
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        plant.water_container_size = wcs
        db.session.commit()


def update_water_container_state(idv, state):
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        if state == 0:
            plant.water_container_state = False
        if state == 1:
            plant.water_container_state = True
        db.session.commit()
