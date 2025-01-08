from flask import Blueprint, render_template

root_bp = Blueprint("root", __name__)

@root_bp.route("/", methods=["GET"])
def home():
    data = "some random data string"

    return render_template("index.html", data=data)

@root_bp.route("/get-response", methods=["POST"])
def get_response():
    return render_template("components/get-response.html")
