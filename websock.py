# ws_client.py
import socketio
import time
import base64
import time

# Replace with your cloud server’s address:
CLOUD_URL = 'http://localhost:5000'

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
    Reads `image1.png`, encodes it as Base64,
    and emits it over the existing Socket.IO connection.
    """
    try:
        with open("image1.png", "rb") as imgf:
            b64 = base64.b64encode(imgf.read()).decode("utf-8")
    except FileNotFoundError:
        print("[ws_client] image1.png not found")
        return

    sio.emit('screenshot', {
        'image': b64,
        'timestamp': time.time()
    })
    print("[ws_client] Screenshot sent to cloud")



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
