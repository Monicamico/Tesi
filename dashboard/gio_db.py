from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import null

db = SQLAlchemy()


class ConnectionRequest(db.Model):
    __tablename__ = 'connectionRequest'
    id = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    ping = db.Column(db.Integer)
    pairing = db.Column(db.Integer)


def add_conn_req(idv, pingv, pairingv):
    plant = Plant.query.filter_by(id=idv).first()
    if plant is None:
        conn = ConnectionRequest.query.filter_by(id=idv).first()
        if conn is None:
            db.session.add(ConnectionRequest(id=idv, ping=pingv, pairing=pairingv))
            db.session.commit()
    # se risulta già tra le piante inserite non faccio nulla dei db
    # e invio un avviso (la pianta è già stata registrata)


def delete_conn_req(idv):
    req = ConnectionRequest.query.filter_by(id=idv).first()
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


def add_radio(radio, url_radio):
    r = Radio.query.filter_by(id=radio).first()
    if r is None:
        db.session.add(Radio(id=radio,
                              name=radio,
                              url_radio=url_radio))
        db.session.commit()


class Plant(db.Model):
    __tablename__ = 'plant'
    id = db.Column(db.String(13), primary_key=True, unique=True, nullable=False)
    radio_id = db.Column(db.String(13), nullable=False)
    name = db.Column(db.String(24), unique=True)
    humidity = db.Column(db.Integer())
    temperature = db.Column(db.Integer())
    light = db.Column(db.Integer())
    humidity_min = db.Column(db.Integer)
    humidity_max = db.Column(db.Integer)
    temperature_max = db.Column(db.Integer)
    temperature_min = db.Column(db.Integer)
    light_max = db.Column(db.Integer)
    light_min = db.Column(db.Integer)
    ping = db.Column(db.Integer, nullable=False)
    watering_light = db.Column(db.Integer, default=70)
    water_container_state = db.Column(db.Boolean, nullable=False, default=True)
    water_container_size = db.Column(db.Float, nullable=False, default=0.5)


def add_plant(idv, ping, radio, hum_min=300, hum_max=1000, temp_min=15, temp_max=30, li_min=50, li_max=250, wl=70,
              ws=True,
              wcs=0.5):
    r = Radio.query.filter_by(id=radio).first()
    if r is not None:
        if delete_conn_req(idv) is not None:
            plant = Plant.query.filter_by(id=idv).first()
            if plant is None:
                db.session.add(Plant(id=idv,
                                     radio_id=radio,
                                     name=idv,
                                     ping=ping,
                                     humidity_min=hum_min,
                                     humidity_max=hum_max,
                                     temperature_max=temp_max,
                                     temperature_min=temp_min,
                                     light_max=li_max,
                                     light_min=li_min,
                                     watering_light=wl,
                                     water_container_size=wcs,
                                     water_container_state=ws))
                db.session.commit()


def delete_plant(idv):
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        db.session.delete(plant)
        db.session.commit()


def update_name(idv, name):
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        plant.name = name
        db.session.commit()


def update_hum(idv, ping, humidity):
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        plant.humidity = humidity
        plant.ping = ping
        db.session.commit()


def update_temp(idv, ping, temperature):
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        plant.temperature = temperature
        plant.ping = ping
        db.session.commit()


def update_light(idv, ping, light):
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        plant.light = light
        plant.ping = ping
        db.session.commit()


def update_temp_min(idv, ping, temp_m):
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        plant.temperature_min = temp_m
        plant.ping = ping
        db.session.commit()


def update_temp_max(idv, ping, temp_m):
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        plant.temperature_max = temp_m
        plant.ping = ping
        db.session.commit()


def update_hum_min(idv, ping, hum_m):
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        plant.humidity_min = hum_m
        plant.ping = ping
        db.session.commit()


def update_hum_max(idv, ping, hum_m):
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        plant.humidity_max = hum_m
        plant.ping = ping
        db.session.commit()


def update_light_max(idv, ping, li_m):
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        plant.light_max = li_m
        plant.ping = ping
        db.session.commit()


def update_light_min(idv, ping, li_m):
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        plant.light_min = li_m
        plant.ping = ping
        db.session.commit()


def update_watering_light(idv, ping, wl):
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        plant.watering_light = wl
        plant.ping = ping
        db.session.commit()


def update_water_container_size(idv, ping, wcs):
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        plant.water_container_size = wcs
        plant.ping = ping
        db.session.commit()


def update_ping(idv, ping):
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        plant.ping = ping
        db.session.commit()


def update_water_container_state(idv, ping, state):
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        plant.ping = ping
        if state == 0:
            plant.water_container_state = False
        if state == 1:
            plant.water_container_state = True
        db.session.commit()

