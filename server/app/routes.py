from flask import Blueprint, redirect, url_for, jsonify, render_template, session
from flask_dance.contrib.google import google
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app.oauth import google_bp
from app import login_manager
from dotenv import load_dotenv
import asyncio
from app.utils import create_jwt_token
from app.core.send_websocket_mes import send_ws_message
from oauthlib.oauth2 import OAuth2Error
from oauthlib.oauth2 import TokenExpiredError
import requests , os


load_dotenv()

auth_bp = Blueprint("auth", __name__)
auth_bp.register_blueprint(google_bp, url_prefix="/login")


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@auth_bp.route("/google")
def google_login():
    if not google.authorized:
        return redirect(url_for("auth.google.login"))

    try:
        # Try to fetch the user info from Google
        resp = google.get("/oauth2/v2/userinfo")
        print("Google response:", resp)

        if resp.ok:
            # Handle the successful response
            user_data = resp.json()
            user_id = user_data["id"]
            user_name = user_data.get("name", "Unknown")
            user_email = user_data.get("email", f"{user_id}@google.com")
            print()
            user = User.create_or_update(user_id, user_name, user_email)
            login_user(user)

            # Create JWT Token and store in session
            token = create_jwt_token(user_id)
            print("JWT Token:", token)
            session["jwt_token"] = token

            if google.token.get("refresh_token"):
                session["google_refresh_token"] = google.token["refresh_token"]

            return redirect("/home")
        else:
            return "Google authentication failed!", 401

    except TokenExpiredError:
        # If token expired, check if we have a refresh token
        refresh_token = session.get("google_refresh_token")
        if refresh_token:
            try:
                # Attempt to refresh the access token using the refresh token
                google.refresh_token(
                    'https://oauth2.googleapis.com/token', refresh_token=refresh_token)
                print("Access token refreshed successfully!")
                # Retry fetching the user info after refreshing the token
                return redirect(url_for("auth.google.login"))
            except Exception as e:
                print("Error refreshing token:", e)
                return "Error refreshing the token. Please log in again.", 500
        else:
            return redirect(url_for("auth.google.login"))

    except Exception as e:
        # General exception handling for other errors
        print("OAuth error:", e)
        return f"OAuth error: {str(e)}", 500


@auth_bp.route("/profile")
@login_required
def profile():
    return jsonify({
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email
    })


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("auth.landing"))


@auth_bp.route("/")
def landing():
    return render_template("landing.html")


@auth_bp.route("/login_page")
def login_page():
    return render_template("login.html")


@auth_bp.route("/home")
@login_required
def home():
    """Root route that displays a landing page with login option."""
    user_data = None
    if current_user.is_authenticated:
        user_data = {
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email,
            "isAuthenticated": True
        }
    return render_template("index.html", current_user=user_data)


# @auth_bp.route("/send-message/<msg>")
# @login_required
# def send_message(msg):
#     token = session.get("jwt_token")
#     if not token:
#         return jsonify({"error": "Unauthorized"}), 401
#     asyncio.run(send_ws_message(token, msg))
#     return jsonify({"message": "Message sent only to the user!"})


@auth_bp.route('/chat', methods=['POST'])
@login_required
def chat(request):
    data = request.get_json()
    user_message = data.get('message', '')
    url = os.getenv("CHAT_API_URL")

    try:
        # Forward the request to your API
        api_response = requests.post(
            url,
            json={
                "message": user_message,
                "user_id": current_user.id,
            }
        )
        return api_response.json()
    except Exception as e:
        print(f"Error calling API: {str(e)}")
        return jsonify({
            'message': "I'm sorry, I couldn't process your request. Please try again later.",
            'Thinking': "<Thinking>Error connecting to API server</think>"
        })
