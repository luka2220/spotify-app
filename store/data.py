from flask import session
import requests
import time


class SessionStore:
    """Object for storing and handleing all flask-session data"""

    @staticmethod
    def store_user_data():
        """Retrives the users data from spotify"""
        access_token = session.get("access_token")

        user = requests.get(
            "https://api.spotify.com/v1/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        if user.status_code != 200:
            raise Exception("Error reteiving user data from spotify API")

        session["user_id"] = user.json()["id"]
        session["username"] = user.json()["display_name"]
        session["user_data"] = user.json()

    @staticmethod
    def get_current_user() -> dict[str, str]:
        user_data = session.get("user_data")
        if user_data is None:
            return {}

        user = {
            "Username": user_data["display_name"],
            "Email": user_data["email"],
            "Country": user_data["country"],
            "Followers": user_data["followers"]["total"],
            "Product": user_data["product"],
            "Account Type": user_data["type"],
        }

        return user

    @staticmethod
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
