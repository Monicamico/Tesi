from flask import Flask
from plant import plant


def create_app():
    app = Flask(__name__)
    app.register_blueprint(plant)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(port=5001)




