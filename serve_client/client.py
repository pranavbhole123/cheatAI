# serve_client.py
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
    print("[serve_client] ✅ Connected to /serve namespace")

@sio.event(namespace='/serve')
def disconnect():
    print("[serve_client] ❌ Disconnected from /serve namespace")

@sio.on('welcome', namespace='/serve')
def on_welcome(data):
    print(f"[serve_client] 📬 Server says:", data)

@sio.on('new_screenshot', namespace='/serve')
def on_new_screenshot(data):
    """
    Payload:
      { 'image': '<base64-png-data>',
        'filename': 'screenshot_20250628_142312_123456.png',
        'timestamp': 1729939392.123456 }
    """
    b64      = data.get('image')
    filename = data.get('filename')  # now always present

    if not b64 or not filename:
        print("[serve_client] ⚠️ Malformed payload:", data)
        return

    # Decode and save under the original, unique filename
    path = os.path.join('served_screenshots', filename)
    with open(path, 'wb') as f:
        f.write(base64.b64decode(b64))

    print(f"[serve_client] 📥 Saved screenshot to {path}")

# 2) Connect to the cloud server’s /serve namespace

if __name__ == '__main__':
    CLOUD_URL = 'http://34.131.212.123:5000/serve'  # adjust host/port if needed

    try:
        sio.connect(CLOUD_URL, namespaces=['/serve'])
        sio.wait()  # block forever, handling events
    except Exception as e:
        print("[serve_client] ❌ Error connecting:", e)
