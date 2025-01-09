from flask import Blueprint, redirect, render_template, request, session
import requests
import os

root_bp = Blueprint("root", __name__)


# NOTE: Left off trying to update state on the html pages being rendered.
# Need to create a header component for authorized users to see their username and maybe even profile picture. The welcome text ahould also render differently for authenticated users.


@root_bp.route("/", methods=["GET"])
def home():
    authorized = session.get("authorized")
    data = "some random data string"
    user = None

    print(f"authorized state {authorized}")

    if authorized:
        user = "user123"
        data = "Hello user123"

    return render_template("index.html", data=data, auth=authorized, user=user)


@root_bp.route("/home/authenticated")
def home_authenticated():
    session_state = session.get("state")
    request_state = request.args.get("state")

    if session_state != request_state:
        print("auth state does not match with cache state")
        error = "An internal error occured, please contact developer... ;)"
        return render_template("components/error.html", error=error)

    code = request.args.get(
        "code"
    )  # extracts the `code` query parameter from the incoming request
    credentials = get_access_token(authorization_code=code)
    print(f"credentials response from get_access_token() = {credentials}")
    session["token"] = credentials["access_token"]
    session["authorized"] = True

    return redirect("/")


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
        print(response.json())
        return response.json()
    else:
        print("possible CSRF attack")
        if request.args.get("error") is not None:
            print(request.args.get("error"))
        raise Exception("Failed to obtain Access token")
