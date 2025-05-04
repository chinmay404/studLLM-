from flask import Flask, redirect, url_for, session, jsonify
from flask_dance.contrib.google import make_google_blueprint, google
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import os
import json


def get_google_blueprint():
    try:
        with open('client_secret.json', 'r') as f:
            client_data = json.load(f)
        
        credentials = client_data.get('web', {})
        client_id = credentials.get('client_id', '')
        client_secret = credentials.get('client_secret', '')
        google_bp = make_google_blueprint(
            client_id=client_id,
            client_secret=client_secret,
            redirect_to="google_login"
        )
        return google_bp
    except FileNotFoundError:
        print("Error: client_secret.json file not found!")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON in client_secret.json!")
        return None