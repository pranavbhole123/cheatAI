

from flask import Flask, request
from flask_socketio import SocketIO, emit
import base64
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'replace-with-your-secret'
socketio = SocketIO(app, cors_allowed_origins="*")

# Directories
os.makedirs('received_screenshots', exist_ok=True)
os.makedirs('received_files', exist_ok=True)

# ———————————————————————————————————————————————————————————
# Default namespace: Screenshot upload and broadcast
# ———————————————————————————————————————————————————————————

@socketio.on('connect')
def handle_connect():
    print(f"[{datetime.now()}] Uploader connected: {request.sid}")
    emit('ack', {'message': 'Connected to cloud server'})

@socketio.on('screenshot')
def handle_screenshot(data):
    b64 = data.get('image')
    ts  = data.get('timestamp', datetime.now().timestamp())
    if not b64:
        emit('error', {'message': 'No image data received'})
        return

    filename = datetime.fromtimestamp(ts).strftime("%Y%m%d_%H%M%S.png")
    path = os.path.join('received_screenshots', filename)
    with open(path, 'wb') as f:
        f.write(base64.b64decode(b64))
    print(f"[{datetime.now()}] Saved screenshot to {path}")

    emit('received', {'message': f'Screenshot saved as {filename}'})

    # Broadcast to /serve
    socketio.emit(
        'new_screenshot',
        {
            'image': b64,
            'filename': filename,
            'timestamp': ts
        },
        namespace='/serve'
    )

# ———————————————————————————————————————————————————————————
# /serve namespace: clients receive screenshots
# ———————————————————————————————————————————————————————————

@socketio.on('connect', namespace='/serve')
def serve_connect():
    print(f"[{datetime.now()}] Viewer connected on /serve: {request.sid}")
    emit('welcome', {'message': 'Connected to serve namespace'})

@socketio.on('disconnect', namespace='/serve')
def serve_disconnect():
    print(f"[{datetime.now()}] Viewer disconnected from /serve: {request.sid}")

# ———————————————————————————————————————————————————————————
# /send_file namespace: receive files from clients
# ———————————————————————————————————————————————————————————

@socketio.on('connect', namespace='/send_file')
def send_file_connect():
    print(f"[{datetime.now()}] File sender connected on /send_file: {request.sid}")
    emit('ack', {'message': 'Connected to send_file namespace'})

@socketio.on('file_upload', namespace='/send_file')
def handle_file_upload(data):
    """
    Expected data:
    {
      'filename': 'notes.txt',
      'data': '<base64-string>'
    }
    """
    b64 = data.get('data')
    filename = data.get('filename', 'unnamed_file')

    if not b64:
        emit('error', {'message': 'No file data received'})
        return

    path = os.path.join('received_files', filename)
    with open(path, 'wb') as f:
        f.write(base64.b64decode(b64))
    print(f"[{datetime.now()}] ✅ File received and saved as {path}")

    emit('received', {'message': f'File saved as {filename}'})

    # Broadcast to /recieve_file
    socketio.emit(
        'file_from_c',
        {
            'filename': filename,
            'data': b64
        },
        namespace='/recieve_file'
    )

# ———————————————————————————————————————————————————————————
# /recieve_file namespace: overlay clients receive files
# ———————————————————————————————————————————————————————————

@socketio.on('connect', namespace='/recieve_file')
def file_receiver_connect():
    print(f"[{datetime.now()}] File listener connected on /recieve_file: {request.sid}")
    emit('welcome', {'message': 'Connected to recieve_file namespace'})

@socketio.on('disconnect', namespace='/recieve_file')
def file_receiver_disconnect():
    print(f"[{datetime.now()}] File listener disconnected from /recieve_file: {request.sid}")

# ———————————————————————————————————————————————————————————

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
