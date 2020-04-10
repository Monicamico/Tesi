from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import null

db = SQLAlchemy()


class ConnectionRequest(db.Model):
    __tablename__ = 'connectionRequest'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    ping =  db.Column(db.Integer)


def add_conn_req(idv, pingv):
    conn = ConnectionRequest.query.filter_by(id=idv).first()
    if conn is None:
        db.session.add(ConnectionRequest(id = idv, ping = pingv))
        db.session.commit()


def delete_conn_req(idv):
    req = ConnectionRequest.query.filter_by(id=idv).first()
    if req is None:
        return
    db.session.delete(req)
    db.session.commit()


class Plant(db.Model):
    __tablename__ = 'plant'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    humidity = db.Column(db.Integer)
    temperature = db.Column(db.Integer)
    light = db.Column(db.Integer)
    humidity_min = db.Column(db.Integer)
    humidity_max = db.Column(db.Integer)
    temperature_max = db.Column(db.Integer)
    temperature_min = db.Column(db.Integer)
    light_max = db.Column(db.Integer)
    light_min = db.Column(db.Integer)
    ping = db.Column(db.Integer, nullable=False)


def add_plant(idv, ping, hum_min=300, hum_max=1000, temp_min=15, temp_max=30, li_min=20, li_max=220, ):
    """
    :param idv: serial number of the vase
    :param ping:
    :param hum_min:
    :param hum_max:
    :param temp_min:
    :param temp_max:
    :param li_min:
    :param li_max:
    """
    delete_conn_req(idv)
    db.session.add(Plant(id=idv, ping=ping,
                         humidity_min=hum_min,
                         humidity_max=hum_max,
                         temperature_max=temp_max,
                         temperature_min=temp_min,
                         light_max=li_max,
                         light_min=li_min))

    db.session.commit()


def delete_plant(idv):
    plant = Plant.query.filter_by(id=idv).first()
    db.session.delete(plant)
    db.session.commit()


def update_hum(idv, ping, humidity):
    plant = Plant.query.filter_by(id=idv).first()
    plant.humidity = humidity
    plant.ping = ping
    db.session.commit()


def update_temp(idv, ping, temperature):
    plant = Plant.query.filter_by(id=idv).first()
    plant.temperature = temperature
    plant.ping = ping
    db.session.commit()


def update_light(idv, ping, light):
    plant = Plant.query.filter_by(id=idv).first()
    plant.light = light
    plant.ping = ping
    db.session.commit()


def update_temp_min(idv, ping, temp_m):
    plant = Plant.query.filter_by(id=idv).first()
    plant.temperature_min = temp_m
    plant.ping = ping
    db.session.commit()


def update_temp_max(idv, ping, temp_m):
    plant = Plant.query.filter_by(id=idv).first()
    plant.temperature_max = temp_m
    plant.ping = ping
    db.session.commit()


def update_hum_min(idv, ping, hum_m):
    plant = Plant.query.filter_by(id=idv).first()
    plant.humidity_min = hum_m
    plant.ping = ping
    db.session.commit()


def update_hum_max(idv, ping, hum_m):
    plant = Plant.query.filter_by(id=idv).first()
    plant.humidity_max = hum_m
    plant.ping = ping
    db.session.commit()


def update_light_max(idv, ping, li_m):
    plant = Plant.query.filter_by(id=idv).first()
    plant.light_max = li_m
    plant.ping = ping
    db.session.commit()


def update_light_min(idv, ping, li_m):
    plant = Plant.query.filter_by(id=idv).first()
    plant.light_min = li_m
    plant.ping = ping
    db.session.commit()


def update_ping(idv, ping):
    plant = Plant.query.filter_by(id=idv).first()
    plant.ping = ping
    db.session.commit()