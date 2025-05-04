import json
import websockets
import asyncio
import datetime
import jwt , os

def create_jwt_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.now() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, os.getenv("SECRET_KEY_JWT"), algorithm="HS256")
