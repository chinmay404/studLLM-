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
load_dotenv()



chat_bp = Blueprint("chat", __name__) 
# chat_bp.register_blueprint(chat_bp, url_prefix="/chat")