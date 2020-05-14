from flask import Flask
from constant import DEBUG
from dashboard import dashboard_page
from home import homepage
from connections import connections_page
from plant import plant_id_page
from plants import plants_page
from radios import radios_page
from map import map_page
from radio_settings import radio_settings_page
from plant_settings import settings_page
from gio_db import db, add_plant, add_conn_req, add_radio, update_vase_state


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # suppress pytest warning
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///giovase.db'
    app.config['SECRET_KEY'] = 'keysecret0679623'
    app.register_blueprint(plants_page)
    app.register_blueprint(radios_page)
    app.register_blueprint(plant_id_page)
    app.register_blueprint(homepage)
    app.register_blueprint(connections_page)
    app.register_blueprint(settings_page)
    app.register_blueprint(radio_settings_page)
    app.register_blueprint(map_page)
    app.register_blueprint(dashboard_page)

    db.init_app(app=app)
    """
        if DEBUG:
        db.drop_all(app=app)
    """
    db.create_all(app=app)

    return app


if __name__ == "__main__":

    app = create_app()
    with app.app_context():
        add_conn_req(34,424,345,'')
    app.run(port=5000)

