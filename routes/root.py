from flask import Blueprint, render_template, request
import requests
import os

root_bp = Blueprint("root", __name__)


@root_bp.route("/", methods=["GET"])
def home():
    data = "some random data string"

    return render_template("index.html", data=data)


@root_bp.route("/home/authenticated")
def home_authenticated():
    os_state = os.getenv("state")
    request_state = request.args.get("state")

    if os_state != request_state:
        error = "An internal error occured, please contact developer... ;)"
        return render_template("components/error.html", error=error)

    code = request.args.get(
        "code"
    )  # extracts the `code` query parameter from the incoming request
    credentials = get_access_token(authorization_code=code)
    os.environ["token"] = credentials["access_token"]

    return "You are authenticated with spotify"


def get_access_token(authorization_code):
    """Sends a post request to get the access token from spotify"""

    spotify_request_access_token_url = "https://accounts.spotify.com/api/token/?"
    body = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "redirect_uri": os.getenv("REDIRECT_URI"),
    }

    response = requests.post(spotify_request_access_token_url, data=body)

    if response.status_code == 200:
        return response.json()
    else:
        print("possible CSRF attack")
        if request.args.get("error") is not None:
            print(request.args.get("error"))
        raise Exception("Failed to obtain Access token")
