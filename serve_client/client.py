# serve_client.py
#hi
import os
import base64
from datetime import datetime

import socketio

# Socket.IO client instance
sio = socketio.Client(logger=True, engineio_logger=True)

# Directory to store received images
os.makedirs('served_screenshots', exist_ok=True)

# 1) Handlers for the /serve namespace

@sio.event(namespace='/serve')
def connect():
    print("[serve_client] Connected to /serve namespace")

@sio.event(namespace='/erve')  # typo safety: ignore
def connect_error(data):
    print("[serve_client] Connection failed:", data)

@sio.event(namespace='/serve')
def disconnect():
    print("[serve_client] Disconnected from /serve")

@sio.on('welcome', namespace='/serve')
def on_welcome(data):
    print(f"[serve_client] Server says:", data)

@sio.on('new_screenshot', namespace='/serve')
def on_new_screenshot(data):
    """
    Expected payload:
      { 'image': '<base64-png-data>', 'filename': '20250607_123456.png', 'timestamp': 1234567890.123 }
    """
    b64 = data.get('image')
    filename = data.get('filename') or datetime.now().strftime("%Y%m%d_%H%M%S.png")
    if not b64:
        print("[serve_client] Received event without image data")
        return

    # Decode and save
    path = os.path.join('served_screenshots', filename)
    with open(path, 'wb') as f:
        f.write(base64.b64decode(b64))
    print(f"[serve_client] Saved served screenshot to {path}")

# 2) Connect to the cloud server’s /serve namespace

if __name__ == '__main__':
    CLOUD_URL = 'http://localhost:5000/serve'  # <-- adjust host/port

    try:
        sio.connect(CLOUD_URL, namespaces=['/serve'])
        sio.wait()  # block forever, handling events
    except Exception as e:
        print("[serve_client] Error connecting:", e)
