from flask import Blueprint, redirect
import os
import urllib.parse
import uuid

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET"])
def spotify_login():
    """Sends the user to authenticate them with thier spotify account"""

    os.environ["state"] = str(uuid.uuid4())

    auth_params = {
        "client_id": os.getenv("CLIENT_ID"),
        "response_type": "code",
        "redirect_uri": os.getenv("REDIRECT_URI"),
        "state": os.environ["state"],
        "scope": "user-read-email user-read-private user-top-read",
        "show_dialog": "true",
    }

    auth_url = "https://accounts.spotify.com/authorize/?" + urllib.parse.urlencode(
        auth_params
    )

    return redirect(auth_url)
