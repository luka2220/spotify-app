from flask import Flask
from routes.root import root_bp
from routes.auth import auth_bp
from dotenv import load_dotenv


load_dotenv(".env")


def create_app():
    app = Flask(__name__)

    app.register_blueprint(root_bp)
    app.register_blueprint(auth_bp)

    return app

