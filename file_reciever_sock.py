# file_receiver.py
import socketio
import base64
import os
import time

CLOUD_URL = 'http://localhost:5000'
RECEIVE_NAMESPACE = '/recieve_file'

sio = socketio.Client()

@sio.event(namespace=RECEIVE_NAMESPACE)
def connect():
    print(f"[file_receiver] ✅ Connected to {RECEIVE_NAMESPACE}")

@sio.event(namespace=RECEIVE_NAMESPACE)
def disconnect():
    print(f"[file_receiver] ❌ Disconnected from {RECEIVE_NAMESPACE}")

@sio.on('file_from_c', namespace=RECEIVE_NAMESPACE)
def handle_file(data):
    """
    Receives a file as base64 from the server and saves it.
    """
    filename = data.get('filename')
    filedata = data.get('data')

    if not filename or not filedata:
        print("[file_receiver] ❌ Invalid file data")
        return

    path = os.path.join("received_files", filename)
    os.makedirs("received_files", exist_ok=True)
    with open(path, "wb") as f:
        f.write(base64.b64decode(filedata))

    print(f"[file_receiver] 📥 File saved as: {path}")

def run_file_receiver():
    while True:
        try:
            print("[file_receiver] 🔄 Connecting...")
            sio.connect(CLOUD_URL, namespaces=[RECEIVE_NAMESPACE])
            sio.wait()
        except Exception as e:
            print("[file_receiver] ❌ Connection error:", e)
            time.sleep(5)
