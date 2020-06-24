from flask import Flask
from view.add_user import adduser_page
from view.login import login_manager
from view.login import auth
from view.dashboard import dashboard_page
from view.home import homepage
from view.connections import connections_page
from view.plant import plant_id_page
from view.plants import plants_page
from view.radios import radios_page
from view.radio_settings import radio_settings_page
from view.plant_settings import settings_page
from model.gio_db import db, add_user, add_plant, add_radio, add_type, \
    change_type
from controller.request import request_page
from view.user_settings import user_settings_page
from view.users import users_page


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # suppress pytest warning
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///giovase.db'
    app.config['SECRET_KEY'] = 'keysecret0679623'

    app.register_blueprint(homepage)
    app.register_blueprint(plants_page)
    app.register_blueprint(radios_page)
    app.register_blueprint(plant_id_page)
    app.register_blueprint(connections_page)
    app.register_blueprint(settings_page)
    app.register_blueprint(radio_settings_page)
    app.register_blueprint(map_page)
    app.register_blueprint(dashboard_page)
    app.register_blueprint(request_page)
    app.register_blueprint(users_page)
    app.register_blueprint(adduser_page)
    app.register_blueprint(user_settings_page)
    app.register_blueprint(auth)

    login_manager.init_app(app)

    db.init_app(app=app)
    db.drop_all(app=app)
    db.create_all(app=app)
    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        add_user('Monica','utente23',0)
        add_type('Nessuno', None, None, None, None, None, None)
        add_type('Yucca', 400, 500, 20, 26, 150, 200)
        add_type('Grassa', 400, 500, 20, 26, 150, 200)
        add_radio('radio','urlfinto')
        add_plant('pianta','radio')
        add_plant('pianta1', 'radio')
        change_type('pianta','Yucca','url')
    app.run(host='192.168.1.18', port=5000)

