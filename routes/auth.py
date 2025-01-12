from flask import Blueprint, redirect, session, request, render_template
import os
import urllib.parse
import uuid
import requests
import time

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET"])
def spotify_login():
    """Sends the user to authenticate them with thier spotify account"""
    session["state"] = str(uuid.uuid4())

    auth_params = {
        "client_id": os.getenv("CLIENT_ID"),
        "response_type": "code",
        "redirect_uri": os.getenv("REDIRECT_URI"),
        "state": session["state"],
        "scope": "user-read-email user-read-private user-top-read",
        "show_dialog": "true",
    }

    auth_url = "https://accounts.spotify.com/authorize/?" + urllib.parse.urlencode(
        auth_params
    )

    return redirect(auth_url)


@auth_bp.route("/home/authenticated")
def home_authenticated():
    session_state = session.get("state")
    request_state = request.args.get("state")

    if session_state != request_state:
        print("auth state does not match with cache state")
        error = "An internal error occured, please contact developer... ;)"
        return render_template("components/error.html", error=error)

    code = request.args.get("code")

    credentials = get_access_token(authorization_code=code)
    if credentials is not None:
        session["access_token"] = credentials["access_token"]
        session["authorized"] = True
        session["refresh_token"] = credentials["refresh_token"]
        session["refresh_token_timer"] = time.time()

        return redirect("/")

    return redirect("/logout")


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
        return None


@auth_bp.route("/logout")
def logout():
    """Sends the user to logout from their spotify account"""
    print(f"{session['user_data']['display_name']} logged out")
    session.clear()
    return redirect("https://www.spotify.com/logout/")
