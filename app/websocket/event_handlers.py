from flask_socketio import emit
from app.extensions import socketio

@socketio.on("connect")
def handle_connect():
    print("Client connected")
    emit("connected", {"message": "Connected to server"})