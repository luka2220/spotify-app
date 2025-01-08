from flask import Flask
from routes.root import root_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(root_bp)

    return app

