from math import ceil

import requests as snd_req
from flask import flash
from werkzeug.security import check_password_hash

from model.gio_db import User, db, Plant, ConnectionRequest, Radio, TypePlant


def correct_password_user(username, password):
    """
    :param username:
    :type username: string
    :param password:
    :type password: string
    :return: True if the user's password is correct otherwise False
    :rtype: boolean
    """
    user = User.query.filter_by(username=username).first()
    checked = check_password_hash(user.password, password)
    return checked


def get_user(username):
    """

    :param username: user's username
    :return the user with username equal to the parameter, if it exist, otherwise none.

    """
    user = User.query.filter_by(username=username).first()
    return user


def add_user(username, password, role):
    """
    Add a user into the database

    :param username:
    :param password:
    :param role:
    :return True if the operation was successful otherwise False

    """
    userGet = User.query.filter_by(username=username).first()
    if userGet is None:
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
    return False


def delete_user(username, password):
    """
    Delete the user username.

    :param username:
    :type username: str
    :param password:
    :type password: str
    :return: True if the operation was successful otherwise False
    :rtype: bool

    """
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


def add_conn_req(idv, signalv, pairingv, radio_id):
    """
    - if there is no connection request or a plant with id equal to the idv parameter:
        it adds the connection request and returns the value True.
    - If the connection request with idv was already present:
        controls the signal strength of both requests (new and old).
        If the signal strength of the new request is greater,
        it replaces the old one with the new one and sends the refusal
        operation to the radio of the old connection request,
        otherwise only the pairing number changes.
        In both cases the function returns the value True.
    - If there was already a plant with id equal to idv (parameter):
        send the join request to the associated radio:
        if this request is not successful, the plant is deleted
        and the new connection request is inserted, otherwise it does nothing.
        In this case the function returns the value False.

    :param idv: vase serial number
    :type idv: string
    :param signalv: the value of the request's signal.
    :type signalv: int
    :param pairingv: three-digit random integer
    :type pairingv: int
    :param radio_id: radio serial number
    :type radio_id: string
    :return: True - if there was no connection request with id equal to idv,
             or if it was present, but it has been replaced
             because the signal of the new request is stronger.
             False - if a plant with id equal to idv was present
             and cannot communicate with the associated radio.
    :rtype: boolean

    """
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
            return True
    else:
        try:
            snd_req.put('http://' + url_from_plant(idv) + '/request', json={'request': 'joined', 'serial': idv})
            return False
        except:
            delete_plant(idv)
            db.session.add(ConnectionRequest(id=idv, signal=signalv, pairing=pairingv, radio_id=radio_id))
            db.session.commit()
            return False


def delete_conn_req(idv, radio):
    """
    if present, it eliminates the connection request with id equal to the first parameter
    from the radio with id equal to the second parameter.

    :param idv: connection (plant) serial number
    :type idv: string
    :param radio: radio serial number
    :type radio: string
    :return: None or the deleted request

    """
    req = ConnectionRequest.query.filter_by(id=idv, radio_id=radio).first()
    if req is None:
        return None
    db.session.delete(req)
    db.session.commit()
    return req


def update_radio_name(radio, name):
    """
    Change the name of the radio

    :param radio: radio serial number
    :type radio: string
    :param name: name to associate with the radio
    :type name: string
    :return: True if the operation is successful, otherwise False
    :rtype: boolean

    """
    r = Radio.query.filter_by(name=name).first()
    if r is None:
        r = Radio.query.filter_by(id=radio).first()
        if r is not None:
            r.name = name
            db.session.commit()
            return True
    return False


def update_sleep_time(radio, time):
    """
    Change the sleep-time of the radio

    :param radio: radio serial number
    :type radio: str
    :param time: new sleep time (minutes)
    :type time: int
    :return: True or False
    :rtype: bool

    """
    r = Radio.query.filter_by(id=radio).first()
    if r is not None:
        r.sleep_time = time
        db.session.commit()
        return True
    return False


def update_radio_transmit_power(radio, tr):
    """
    Change the transmit-power of the radio

    :param radio: radio serial number
    :type radio: str
    :param tr: new transmit power
    :type tr: int
    :return: True or False
    :rtype: bool

    """
    r = Radio.query.filter_by(id=radio).first()
    if r is not None:
        if 0 <= tr <= 7:
            r.transmit_power = tr
            db.session.commit()
            return True
    return False


def delete_radio(radio):
    """
    Delete the radio with serial number equal to parameter

    :param radio: serial number
    :type radio: str
    :return: True or False
    :rtype: bool

    """
    r = Radio.query.filter_by(id=radio).first()
    if r is not None:
        db.session.delete(r)
        db.session.commit()
        return True
    return False


def add_radio(radio, url_radio):
    """
    - If the radio is not in the database:
        add it, and return the value True.
    - If the radio is already present:
        - if the url has not changed: it does nothing and returns the False value,
        - if the url has changed: change url and reset all the parameters, return the False value

    :param radio: serial number
    :type radio: str
    :param url_radio: raspberry (radio) url
    :type url_radio: str
    :return: True or False
    :rtype: bool

    """
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
    """
    Gets the radio url.

    :param radio: serial number
    :type radio: string
    :return: the url of the radio or None
    :rtype: string

    """
    r = Radio.query.filter_by(id=radio).first()
    if r is not None:
        return r.url_radio
    else:
        return None


def radio_from_url(url):
    """
    Gets the radio with url equal to parameter.

    :param url: raspberry-radio url
    :type url: str
    :return: object radio or None
    :rtype: radio

    """
    r = Radio.query.filter_by(url_radio=url).first()
    return r


def associated_plants(radio_id):
    """
    Gets plants list associated with the radio

    :param radio_id: radio serial number
    :type radio_id:
    :return: the list of plants associated with the radio
    :rtype: plant list

    """
    plants = Plant.query.filter_by(radio_id=radio_id).all()
    return plants


def add_plant(idv, radio):
    """
    if the radio with serial number equal to the second parameter exists
    and the plant doesn't exist, adds the plant with serial number equal
    to idv, and deletes the connection request with id equal to idv.

    :param idv: plant serial number
    :type idv: string
    :param radio: radio serial number
    :type radio: string

    """
    r = Radio.query.filter_by(id=radio).first()
    if r is not None:
        plant = Plant.query.filter_by(id=idv).first()
        if plant is None:
            db.session.add(Plant(id=idv,
                                 radio_id=radio,
                                 name=idv,
                                 state_fitness=None,
                                 typeplant_id='Nessuno',
                                 humidity=None,
                                 light=None,
                                 temperature=None,
                                 ideal_h=None,
                                 ideal_l=None,
                                 ideal_t=None,
                                 humidity_min=250,
                                 humidity_max=410,
                                 temperature_max=30,
                                 temperature_min=25,
                                 light_max=250,
                                 light_min=50,
                                 watering_light=70,
                                 water_container_size=0.5,
                                 water_container_state=True,
                                 transmit_power=5,
                                 send_time=15))
            db.session.commit()
            plant = Plant.query.filter_by(id=idv).first()
            if plant is not None:
                plant.ideal_h = ceil((plant.humidity_max + plant.humidity_min) / 2)
                plant.ideal_t = ceil((plant.temperature_max + plant.temperature_min) / 2)
                plant.ideal_l = ceil((plant.light_max + plant.light_min) / 2)
                db.session.commit()
            delete_conn_req(idv, radio)


def url_from_plant(idv):
    """
    Gets the url of the associated raspberry-radio.

    :param idv: plant serial number
    :type idv: str
    :return: url or -1
    :rtype: str

    """
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        radio = Radio.query.filter_by(id=plant.radio_id).first()
        if radio is not None:
            return 'http://' + radio.url_radio
    return -1


def delete_plant(idv):
    """
    Delete the plant with serial number equal to idv, if presents.

    :param idv: plant serial number
    :type idv: str

    """
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        db.session.delete(plant)
        db.session.commit()


def update_name(idv, name):
    """
    Change the plant's name.

    :param idv: plant serial number
    :type idv: str
    :param name: new name
    :type name: str
    :return: True (success) or False
    :rtype: bool

    """
    plant = Plant.query.filter_by(name=name).first()
    if plant is None:
        plant = Plant.query.filter_by(id=idv).first()
        if plant is not None:
            plant.name = name
            db.session.commit()
            return True
    return False


def change_type(idv, idt, url):
    """
    Change the type of the plant

    :param idv: plant serial number
    :type idv: str
    :param idt: type of plant id
    :type idt: int
    :param url: associated radio's url
    :type url: str
    :return: True in case of success, otherwise False
    :rtype: bool

    """
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        type = TypePlant.query.filter_by(id=idt).first()
        if type is not None:
            if idt != 'Nessuno':
                try:
                    snd_req.put(url + '/request',
                                json=dict(request='light_max', serial=idv, param=type.light_max))

                    snd_req.put(url + '/request',
                                json=dict(request='light_min', serial=idv, param=type.light_min))

                    snd_req.put(url + '/request',
                                json=dict(request='hum_min', serial=idv, param=type.humidity_min))

                    snd_req.put(url + '/request',
                                json=dict(request='hum_max', serial=idv, param=type.humidity_max))

                    snd_req.put(url + '/request',
                                json=dict(request='temp_max', serial=idv, param=type.temperature_max))

                    snd_req.put(url + '/request',
                                json=dict(request='temp_min', serial=idv, param=type.temperature_min))

                    plant.typeplant_id = idt
                    db.session.commit()
                except:
                    return False
            return True
    return False


def update_vase_transmit_power(idv, tr):
    """
    Change the radio transmit power of the plant

    :param idv: serial number
    :type idv: str
    :param tr: value of the new transmit power
    :type tr: int
    :return: True or False
    :rtype: bool

    """
    p = Plant.query.filter_by(id=idv).first()
    if p is not None:
        p.transmit_power = tr
        db.session.commit()
        return True
    return False


def update_send_time(idv, st):
    """

    :param idv: plant serial number
    :type idv: str
    :param st: send time interval, minutes
    :type st: int

    """
    p = Plant.query.filter_by(id=idv).first()
    if p is not None:
        p.send_time = st
        db.session.commit()


def update_hum(idv, humidity):
    """

    :param idv: plant serial number
    :type idv: str
    :param humidity: humidity measure
    :type humidity: int

    """
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        plant.humidity = humidity
        update_plant_state_fitness(idv)
        db.session.commit()


def update_temp(idv, temperature):
    """

    :param idv: plant serial number
    :type idv: str
    :param temperature: temperature measure
    :type temperature: int

    """
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        plant.temperature = temperature
        update_plant_state_fitness(idv)
        db.session.commit()


def update_light(idv, light):
    """

    :param idv: plant serial number
    :type idv: str
    :param light: light measure
    :type light: int

    """
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        plant.light = light
        update_plant_state_fitness(idv)
        db.session.commit()


def update_ideal_hum(idv, ideal_humidity):
    """

    :param idv: plant serial number
    :type idv: str
    :param ideal_humidity:
    :type ideal_humidity: int

    """
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        plant.ideal_h = ideal_humidity
        db.session.commit()
        update_plant_state_fitness(idv)


def update_ideal_light(idv, ideal_light):
    """

    :param idv: plant serial number
    :type idv: str
    :param ideal_light:
    :type ideal_light:

    """
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        plant.ideal_l = ideal_light
        db.session.commit()
        update_plant_state_fitness(idv)


def update_ideal_temp(idv, ideal_temp):
    """

    :param idv: plant serial number
    :type idv: str
    :param ideal_temp:
    :type ideal_temp:

    """
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        plant.ideal_t = ideal_temp
        db.session.commit()
        update_plant_state_fitness(idv)


def update_plant_state_fitness(idv):
    """
    Update the plant status, calculated with the values of:
        - ideal humidity, ideal light, ideal temperature
        - current humidity, current light, current temperature

    :param idv: serial number
    :type idv: str
    :return: the fitness state
    :rtype: float

    """
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:

        if (plant.humidity is not None) and (plant.temperature is not None) and (plant.light is not None):
            ideal_humidity: int = plant.ideal_h
            ideal_temperature: int = plant.ideal_t
            ideal_light = plant.ideal_l

            hum = abs(int(plant.humidity) - ideal_humidity) / ideal_humidity
            temp = abs(plant.temperature - ideal_temperature) / ideal_temperature
            lig = abs(int(plant.light) - ideal_light) / ideal_light

            state_fitness = (hum + temp + lig) / 3
            state_fitness = round(state_fitness, 2)
            plant.state_fitness = 1 - state_fitness
            db.session.commit()

            return state_fitness
        return None
    return None


def update_temp_min(idv, temp_m):
    """

    """
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        plant.temperature_min = temp_m
        db.session.commit()


def update_temp_max(idv, temp_m):
    """ """
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        plant.temperature_max = temp_m
        db.session.commit()


def update_hum_min(idv, hum_m):
    """ """
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        plant.humidity_min = hum_m
        db.session.commit()


def update_hum_max(idv, hum_m):
    """ """
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        plant.humidity_max = hum_m
        db.session.commit()


def update_light_max(idv, li_m):
    """ """
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        plant.light_max = li_m
        db.session.commit()


def update_light_min(idv, li_m):
    """ """
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        plant.light_min = li_m
        db.session.commit()


def update_watering_light(idv, wl):
    """ """
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        plant.watering_light = wl
        db.session.commit()


def update_water_container_size(idv, wcs):
    """ """
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        plant.water_container_size = wcs
        db.session.commit()


def update_water_container_state(idv, state):
    """ """
    plant = Plant.query.filter_by(id=idv).first()
    if plant is not None:
        if state == 0:
            plant.water_container_state = False
        if state == 1:
            plant.water_container_state = True
        db.session.commit()


def add_type(idt, hum_min, hum_max, temp_min, temp_max, light_min, light_max):
    """
    Adds a new type of plant

    :param idt: id (name) of the type
    :type idt: str
    :param hum_min: min. humidity of the type
    :type hum_min: int
    :param hum_max: max. humidity of the type
    :type hum_max: int
    :param temp_min: min. temperature of the type
    :type temp_min: int
    :param temp_max: max. temperature of the type
    :type temp_max: int
    :param light_max: max. light of the type
    :type light_max: int
    :param light_min: min. light of the type
    :type light_min: int

    """
    t = TypePlant.query.filter_by(id=idt).first()

    light_max = round(int(light_max) / 100 * 255)
    light_min = round(int(light_min) / 100 * 255)
    hum_max = round(int(hum_max) / 100 * 1023)
    hum_min = round(int(hum_min) / 100 * 1023)
    temp_max = int(temp_max)
    temp_min = int(temp_min)

    if t is None:
        db.session.add(TypePlant(id=idt,
                                 humidity_min=hum_min,
                                 humidity_max=hum_max,
                                 temperature_max=temp_max,
                                 temperature_min=temp_min,
                                 light_max=light_max,
                                 light_min=light_min))
        db.session.commit()
