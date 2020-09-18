from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from model.constant import Role
db = SQLAlchemy()


class User(db.Model):
    """
    Represent one user.

    Params:
        - id
        - username
        - password
        - role
        - is_active: boolean
        - is_anonymous: boolean

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
        """
        it returns true if the user is already authenticated, otherwise false
        :return: self.is_authenticated
        :rtype: true or false
        """
        return self.is_authenticated

    def set_password(self, password):
        """
        set the password of the user
        :param: password: user password
        :type: password: string
        """
        self.password = generate_password_hash(password)
        db.session.commit()

    @property
    def is_admin(self):
        """
        check if the user is admin
        :return: True or False
        """
        if self.role == Role.ADMIN.value:
            return True
        else:
            return False

    def authenticate(self, password):
        """
        if the password provided is correct, it authenticates the user
        :param: password: user password
        :type: password: string
        :return: True or False
        """
        # print(password, " ", self.password)
        checked = check_password_hash(self.password, password)
        self.is_authenticated = checked
        return self.is_authenticated

    def get_id(self):
        """
        :return: the user id
        :rtype: Integer
        """
        return self.id

    def get_username(self):
        """
        :return: the user's username
        :rtype: String
        """
        return self.username

    def set_username(self,username):
        """
        it sets the user username
        :param username: new username
        :type username: string
        :return: true if username has been set, otherwise false
        :rtype: Boolean
        """
        try:
            self.username = username
            db.session.commit()
            return True
        except:
            return False

    def set_role(self,role):
        """
        It sets the user role
        :param role: the role
        :type role: value of the enum Role
        :return: True if the user's role has been set, otherwise false
        :rtype: Boolean
        """
        try:
            self.role = role
            db.session.commit()
            return True
        except:
            return False


class ConnectionRequest(db.Model):
    """
   A class used to represent a connection request from plant

   Params:
    - id : String, vase serial number
    - signal: int, the value of the request's signal, ranges from -128 to -42. -128 means a weak signal and -42 means a strong one.
    - pairing: int, three-digit random integer, representing the connection request of the plant.
    - radio_id : String,  radio serial number

    """
    __tablename__ = 'connectionRequest'
    id = db.Column(db.String, primary_key=True, nullable=False)
    # the value of the signal ranges from -128 to -42
    # (-128 means a weak signal and -42 means a strong one.)
    signal = db.Column(db.Integer)
    pairing = db.Column(db.Integer)
    radio_id = db.Column(db.String, primary_key=True)


class Radio(db.Model):
    """
    A class used to represent the radio-raspberry

    Params:
        - id: String, radio serial number
        - name: string, radio name
        - url_radio: string, raspberry url used to communicate operation request to the radio and to the associated plants
        - transmit_power : int, radio transmission power, range 0-7 (lower, higher)
        - sleep_time: time interval in which the radio is in sleep state (minutes)

    """
    __tablename__ = 'radio'
    id = db.Column(db.String(13), primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(24), unique=True)
    url_radio = db.Column(db.String(), nullable=False)
    transmit_power = db.Column(db.Integer(), default=7)
    sleep_time = db.Column(db.Integer(), default=10)


class Plant(db.Model):
    """
     A class used to represent the plant
    """
    __tablename__ = 'plant'
    id = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    radio_id = db.Column(db.String(13), nullable=False)
    typeplant_id = db.Column(db.String, db.ForeignKey('TypePlant.id'))
    name = db.Column(db.String(24), unique=True)
    state_fitness = db.Column(db.Float)
    humidity = db.Column(db.Integer)
    temperature = db.Column(db.Integer)
    light = db.Column(db.Integer)
    ideal_h = db.Column(db.Integer)
    ideal_t = db.Column(db.Integer)
    ideal_l = db.Column(db.Integer)
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


class TypePlant(db.Model):
    """
    Represent the type of plant
    """
    __tablename__ = 'TypePlant'
    id = db.Column(db.String, primary_key=True)
    plants = db.relationship('Plant', backref='TypePlant')
    humidity_min = db.Column(db.Integer)
    humidity_max = db.Column(db.Integer)
    temperature_max = db.Column(db.Integer)
    temperature_min = db.Column(db.Integer)
    light_max = db.Column(db.Integer)
    light_min = db.Column(db.Integer)

    @property
    def is_none(self):
        if self.id == 'None':
            return True
        else:
            return False


