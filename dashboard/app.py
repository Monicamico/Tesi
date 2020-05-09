from flask import Flask
from constant import DEBUG
from home import homepage
from connections import connections_page
from plant import plant_id_page
from plants import plants_page
from radios import radios_page
from settings import settings_page
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

    db.init_app(app=app)
    if DEBUG:
        db.drop_all(app=app)
    db.create_all(app=app)

    return app


if __name__ == "__main__":

    app = create_app()
    with app.app_context():
        add_radio(4850,'dsaa')
        add_conn_req(3456, 454, 345)
        add_plant(3456, 5642, 4850)
        add_conn_req(3457, 474, 345)
        add_plant(3457, 6322, 4850)
        update_vase_state(3457, 798, 0)
        add_conn_req(3467, 474, 345)
        add_plant(3467, 6322, 4850)
        update_vase_state(3467, 798, 0)
        
        add_conn_req(5678, 474, 345)
        add_conn_req(8910, 474, 345)
        add_conn_req(1234, 474, 345)
        add_conn_req(2345, 474, 345)
        add_conn_req(4567, 474, 345)
      
        add_plant(5678, 6322, 4850)
        add_plant(1234, 6322, 4850)
        add_plant(2345, 6322, 4850)
        add_plant(4567, 6322, 4850)
        add_plant(8910, 6322, 4850)
        """
        add_conn_req(1000, 474, 345)
        add_conn_req(1002, 474, 345)
        add_conn_req(1003, 474, 345)
        add_conn_req(1004, 474, 345)
        add_plant(1000, 6322, 4850)
        add_plant(1002, 6322, 4850)
        add_plant(1003, 6322, 4850)
        add_plant(1004, 6322, 4850)
        """


    app.run(port=5000)

