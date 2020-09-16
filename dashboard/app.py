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
from model.gio_db import db
from controller.utility import add_user, add_radio, add_plant, change_type, add_type, update_hum, update_light, \
    update_temp
from controller.request import request_page
from view.user_settings import user_settings_page
from view.users import users_page
import csv


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
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
    with open('PlantTypesData.txt', mode='r') as plantType_file:
        csv_reader = csv.reader(plantType_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                with app.app_context():
                    add_type(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            line_count += 1
        print(f'Processed {line_count} lines.')
    with app.app_context():
        add_user('Admin', 'admin', 0)
        add_user('Monica', 'utente23', 1)
    app.run(host='127.0.0.1',port=5000)
