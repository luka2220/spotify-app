from flask import Flask
from routes.root import root_bp
from routes.auth import auth_bp
from dotenv import load_dotenv
from flask_session import Session


load_dotenv(".env")


def create_app():
    app = Flask(__name__)

    # Application session configuration
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    app.register_blueprint(root_bp)
    app.register_blueprint(auth_bp)

    return app
