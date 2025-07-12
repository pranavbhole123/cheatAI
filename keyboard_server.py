# keyboard_ws_server.py

from flask import Flask, request
from flask_socketio import SocketIO, emit
from datetime import datetime




app = Flask(__name__)
app.config['SECRET_KEY'] = 'keyboard-relay-secret'
socketio = SocketIO(app, cors_allowed_origins="*")

# Namespace for keyboard communication
KEYBOARD_NAMESPACE = '/keyboard'

@socketio.on('connect', namespace=KEYBOARD_NAMESPACE)
def on_connect():
    print(f"[{datetime.now()}] ✅ Client connected on /keyboard: {request.sid}")
    emit('ack', {'message': 'Connected to /keyboard'})

@socketio.on('disconnect', namespace=KEYBOARD_NAMESPACE)
def on_disconnect():
    print(f"[{datetime.now()}] ❌ Client disconnected from /keyboard: {request.sid}")


@socketio.on('message', namespace=KEYBOARD_NAMESPACE)
def on_message(data):
    print(f"[{datetime.now()}] 🔁 Relaying message: {data}")
    # Relay message based on content
    if data == "go":
        socketio.emit('go', data, namespace=KEYBOARD_NAMESPACE)
    elif data == "esc":
        socketio.emit('esc', data, namespace=KEYBOARD_NAMESPACE)
    elif data == "trigger":
        socketio.emit('trigger', data, namespace=KEYBOARD_NAMESPACE)
    elif data=="mcq":
        socketio.emit('mcq', data, namespace=KEYBOARD_NAMESPACE)
    elif data=="up":
        socketio.emit('up', data, namespace=KEYBOARD_NAMESPACE)
    elif data=="down":
        socketio.emit('down', data, namespace=KEYBOARD_NAMESPACE)
    else:
        socketio.emit('message', data, namespace=KEYBOARD_NAMESPACE)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5050)
