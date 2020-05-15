from flask_sqlalchemy import SQLAlchemy
import requests as snd_req

db = SQLAlchemy()


class ConnectionRequest(db.Model):
    __tablename__ = 'connectionRequest'
    id = db.Column(db.String, primary_key=True, nullable=False)
    ping = db.Column(db.Integer)
    pairing = db.Column(db.Integer)
    url = db.Column(db.String, primary_key=True)


def url_from_conn(idv):
    c = ConnectionRequest.query.filter_by(id=idv).first()
    if c is not None:
        return c.url
    else:
        return -1


def add_conn_req(idv, pingv, pairingv, urlv):
    plant = Plant.query.filter_by(id=idv).first()
    if plant is None:
        conn = ConnectionRequest.query.filter_by(id=idv).first()
        if conn is None:
            db.session.add(ConnectionRequest(id=idv, ping=pingv, pairing=pairingv, url=urlv))
            db.session.commit()
            return True
        else:
            conn.pairing = pairingv
            conn.ping = pingv
            conn.url = urlv
            db.session.commit()
    else:
        url = url_from_plant(idv)
        if url != urlv:
            snd_req.put(url + '/request', json={'request': 'deleted', 'serial': idv})
            plant.url_radio = urlv
        snd_req.put(urlv + '/request', json={'request': 'joined', 'serial': idv})


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
    transmit_power = db.Column(db.Integer(), default=7)
    sleep_time = db.Column(db.Integer(), default=10)


def update_radio_name(radio,name):
    r = Radio.query.filter_by(name=name).first()
    if r is None:
        r = Radio.query.filter_by(id=radio).first()
        if r is not None:
            r.name = name
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
    r = Radio.query.filter_by(id=radio).first()
    if r is None:
        db.session.add(Radio(id=radio, name=radio,
                             url_radio=url_radio,
                             transmit_power=7,
                             sleep_time=10))
        db.session.commit()
    else:
        radio_with_url = Radio.query.filter_by(id=radio, url_radio=url_radio).first()
        #the url of the radio is changed
        if radio_with_url is None:
            r.url_radio = url_radio
            r.transmit_power = 7
            r.sleep_time = 10
            db.session.commit()


def url_from_radio(radio):
    r = Radio.query.filter_by(id=radio).first()
    if r is not None:
        return r.url_radio
    else:
        return None


class Plant(db.Model):
    __tablename__ = 'plant'
    id = db.Column(db.String(13), primary_key=True, unique=True, nullable=False)
    radio_id = db.Column(db.String(13), nullable=False)
    name = db.Column(db.String(24), unique=True)
    state = db.Column(db.Boolean)
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
    transmit_power = db.Column(db.Integer(), default=7)


def add_plant(idv, ping, radio):
    r = Radio.query.filter_by(id=radio).first()
    if r is not None:
        if delete_conn_req(idv) is not None:
            plant = Plant.query.filter_by(id=idv).first()
            if plant is None:
                db.session.add(Plant(id=idv,
                                     radio_id=radio,
                                     name=idv,
                                     ping=ping,
                                     state=True,
                                     humidity_min=300,
                                     humidity_max=1000,
                                     temperature_max=30,
                                     temperature_min=15,
                                     light_max=250,
                                     light_min=50,
                                     watering_light=70,
                                     water_container_size=0.5,
                                     water_container_state=True,
                                     transmit_power=7))
                db.session.commit()


def url_from_plant(idv):
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        radio = Radio.query.filter_by(id=plant.radio_id).first()
        if radio is not None:
            return radio.url_radio
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


def update_vase_state(idv, ping, state):
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        if state == 0:
            plant.state = False
        else:
            plant.state = True
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

