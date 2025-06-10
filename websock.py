# ws_client.py
import socketio
import time
import base64
import time
from dotenv import load_dotenv
import os

# Replace with your cloud server’s address:
load_dotenv()
CLOUD_URL = os.getenv("WEB_SOCKET_SERVER_URL")
print(CLOUD_URL)

# This is the global Socket.IO client you’ll reuse everywhere
sio = socketio.Client()

@sio.event
def connect():
    print("🔌 WebSocket connected to", CLOUD_URL)

@sio.event
def disconnect():
    print("🔌 WebSocket disconnected")

@sio.on('ack')
def on_ack(data):
    print("📬 Ack from cloud:", data)



def send_screenshot():
    """
    Reads all images in the `query` folder, encodes them as Base64,
    and emits each over the existing Socket.IO connection.
    """
    image_dir = "query"
    if not os.path.exists(image_dir):
        print("[ws_client] 'query' folder does not exist.")
        return

    image_files = sorted([
        f for f in os.listdir(image_dir)
        if f.lower().endswith(('.png', '.jpg', '.jpeg'))
    ])

    if not image_files:
        print("[ws_client] No screenshots to send.")
        return

    for filename in image_files:
        path = os.path.join(image_dir, filename)
        try:
            with open(path, "rb") as imgf:
                b64 = base64.b64encode(imgf.read()).decode("utf-8")
        except Exception as e:
            print(f"[ws_client] ❌ Failed to read {filename}: {e}")
            continue

        sio.emit('screenshot', {
            'image': b64,
            'filename': filename,
            'timestamp': time.time()
        })
        print(f"[ws_client] 📤 Sent {filename} to cloud")



def run_ws():
    """
    Connect to the cloud WebSocket and stay connected.
    Calling `sio.wait()` here blocks this thread,
    but does not block your main or Flask threads.
    """
    while True:
        try:
            print("🔄 Attempting WS connect...")
            sio.connect(CLOUD_URL)
            # This will block until the connection is closed,
            # then loop around and retry
            sio.wait()
        except Exception as e:
            print("❌ WS connection error:", e)
            time.sleep(5)
