from flask import Flask, jsonify, render_template, Blueprint
from constant import DEBUG
from home import homepage
from connections import connections_page
from plant import plant_id_page
from plants import plants_page
from gio_db import db, add_plant, add_conn_req


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # suppress pytest warning
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///giovase.db'

    app.register_blueprint(plants_page)
    app.register_blueprint(plant_id_page)
    app.register_blueprint(homepage)
    app.register_blueprint(connections_page)

    db.init_app(app=app)
    if DEBUG:
        db.drop_all(app=app)
    db.create_all(app=app)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(port=5000)


