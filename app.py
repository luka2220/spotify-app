from datetime import timedelta
from flask import Flask
from routes.root import root_bp
from routes.auth import auth_bp
from dotenv import load_dotenv
from flask_session import Session


load_dotenv(".env")


def create_app():
    app = Flask(__name__)

    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=80)
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    Session(app)

    app.register_blueprint(root_bp)
    app.register_blueprint(auth_bp)

    return app
