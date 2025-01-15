from flask import Blueprint, render_template, request, session
from store.data import SessionStore
import time

root_bp = Blueprint("root", __name__)


@root_bp.before_request
def before_profile_request():
    """Executes before every request to all routes in root_bp"""

    is_authorized = session.get("authorized")
    token_last_refreshed = session.get("refresh_token_timer")

    if is_authorized and token_last_refreshed:
        if time.time() - token_last_refreshed > 3600.00:
            SessionStore.refresh_token()

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
        SessionStore.store_user_data()
        data = f"welcome {session['username']}"
        user = session["username"]

    return render_template("index.html", data=data, auth=authorized, user=user)


@root_bp.route("/profile", methods=["GET"])
def profile_data():
    """Renders the profile page with users spotify data and top playlists and songs"""

    spotify_profile_link = session["user_data"]["external_urls"]["spotify"]
    user_profile = SessionStore.get_current_user()
    if user_profile is None:
        msg = "Signin to access your profile"
        return render_template("components/error", error=msg), 401

    return render_template(
        "components/profile.html",
        profile_data=SessionStore.get_current_user(),
        spotify_profile_link=spotify_profile_link,
    )
