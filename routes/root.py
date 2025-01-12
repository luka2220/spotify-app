from flask import Blueprint, render_template, request, session
import requests
import time

root_bp = Blueprint("root", __name__)


@root_bp.before_request
def before_profile_request():
    if session.get("authorized") and session.get("refresh_token_timer"):
        if (
            session["authorized"]
            and time.time() - session["refresh_token_timer"] > 3600.00
        ):
            refresh_token()

    if request.path == "/profile":
        user = session.get("username")
        if not user:
            return "Signin to access your profile", 403


@root_bp.route("/", methods=["GET"])
def home():
    authorized = session.get("authorized")
    data = "some random data string"
    user = None

    if authorized:
        store_user_data()
        data = f"welcome {session['username']}"
        user = session["username"]

    return render_template("index.html", data=data, auth=authorized, user=user)


@root_bp.route("/profile", methods=["GET"])
def profile_data():
    """Renders the profile page with users spotify data and top playlists and songs"""
    user_data = session["user_data"]
    spotify_profile_link = session["user_data"]["external_urls"]["spotify"]
    profile_data = {
        "Username": user_data["display_name"],
        "Email": user_data["email"],
        "Country": user_data["country"],
        "Followers": user_data["followers"]["total"],
        "Product": user_data["product"],
        "Account Type": user_data["type"],
    }

    return render_template(
        "components/profile.html",
        profile_data=profile_data,
        spotify_profile_link=spotify_profile_link,
    )


def store_user_data():
    """Retrives the users data from spotify"""
    user = requests.get(
        "https://api.spotify.com/v1/me",
        headers={"Authorization": f"Bearer {session['access_token']}"},
    )

    if user.status_code != 200:
        raise Exception("Error reteiving user data from spotify API")

    session["user_id"] = user.json()["id"]
    session["username"] = user.json()["display_name"]
    session["user_data"] = user.json()


def refresh_token():
    """Sends a request to the spotify API to refresh our access token"""
    credentials = requests.post(
        "https://accounts.spotify.com/api/token",
        headers={
            "grant_type": "refresh_token",
            "refresh_token": session["refresh_token"],
        },
    )

    if credentials.status_code == 200:
        credentials_json = credentials.json()
        session["access_token"] = credentials_json["access_token"]
        session["authorized"] = True
        session["refresh_token"] = credentials_json["refresh_token"]
        session["refresh_token_timer"] = time.time()
