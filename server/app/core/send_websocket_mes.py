import json
import websockets
import asyncio
from urllib.parse import quote

async def send_ws_message(token, message):
    uri = f"ws://127.0.0.1:8000/ws?token={quote(token)}"
    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send(json.dumps({"message": message}))
            print(f"Sent message: {message}")

            response = await websocket.recv()
            print("Received response from WebSocket:", response)

            return json.loads(response) 

    except json.JSONDecodeError:
        return {"error": "Invalid response format"}
    except Exception as e:
        return {"error": "WebSocket connection error"}
