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
from gio_db import db, add_conn_req, delete_conn_req, delete_plant, add_radio, add_plant, update_vase_state
from request import request_page


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
    app.register_blueprint(request_page)

    db.init_app(app=app)


    """
     if DEBUG:
        db.drop_all(app=app)
        add_radio(1, 'urlradio1')
        add_conn_req(20, 11, 345, 'urlradio1')
        add_plant(20, 1, 5)
           
        add_radio(2, 'urlradio2')
        add_radio(3, 'urlradio3')
        add_radio(4, 'urlradio4')
        add_radio(5, 'urlradio5')
        add_radio(6, 'urlradio6')
        add_conn_req(10, 11, 345, 'urlradio1')
        add_plant(10,1,1)
        add_conn_req(11,11,345,'urlradio1')
        add_plant(11,1,1)
        add_conn_req(12,12,432,'urlradio2')
        add_plant(12,1,1)
        add_conn_req(13, 11, 345, 'urlradio1')
        add_plant(13,11,1)
        add_conn_req(14, 11, 345, 'urlradio1')
        add_plant(14,1,2)
        add_conn_req(15, 11, 345, 'urlradio1')
        add_plant(15,1,3)
        add_conn_req(16, 11, 345, 'urlradio2')
        add_plant(16,1,3)
        add_conn_req(17, 11, 345, 'urlradio2')
        add_plant(17,1,3)
        add_conn_req(18, 11, 345, 'urlradio1')
        add_plant(18,1,3)
       
        add_conn_req(31, 11, 345, 'urlradio1')
        add_plant(31,1,5)
        add_conn_req(32, 11, 345, 'urlradio1')
        add_plant(32,1,5)
        add_conn_req(19, 11, 345, 'urlradio1')
        add_plant(19,1,5)
        
        add_conn_req(21, 11, 345, 'urlradio1')
        add_plant(21,1,5)
        add_conn_req(22, 11, 345, 'urlradio1')
        add_plant(22,1,5)
        add_conn_req(23, 11, 345, 'urlradio1')
        add_plant(23,4,4)
        add_conn_req(24, 11, 345, 'urlradio1')
        add_plant(24,1,6)
        add_conn_req(25, 11, 345, 'urlradio1')
        add_plant(25,1,6)
        add_conn_req(26, 11, 345, 'urlradio1')
        add_plant(26,4,6)
        add_conn_req(27, 11, 345, 'urlradio1')
        add_plant(27,1,4)
        add_conn_req(28, 11, 345, 'urlradio1')
        add_plant(28,1,6)
        add_conn_req(29, 11, 345, 'urlradio1')
        add_plant(29,1,6)
         with app.app_context():
        update_vase_state(25,1,0)
        update_vase_state(22, 1, 0)
        update_vase_state(24, 1, 0)
        update_vase_state(13, 1, 0)
        update_vase_state(15, 1, 0)
        update_vase_state(14, 1, 0)
         with app.app_context():
        add_conn_req(34, 11, 345, 'urlradio1')
        add_plant(34, 1, 2)
        add_conn_req(35, 11, 345, 'urlradio1')
        add_plant(35, 1, 2)
        add_conn_req(36, 11, 345, 'urlradio1')
        add_plant(36, 1, 2)

    """
    db.create_all(app=app)
    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        delete_conn_req(20)
    app.run(port=5000)

