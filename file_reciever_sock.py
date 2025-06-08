# file_receiver.py
import socketio
import base64
import os
import time
from dotenv import load_dotenv


load_dotenv()
CLOUD_URL = os.getenv("WEB_SOCKET_SERVER_URL")
print(CLOUD_URL)
RECEIVE_NAMESPACE = '/recieve_file'

third_ans=""

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
    Also stores its decoded content in `third_ans`.
    """
    global third_ans
    
    filename = data.get('filename')
    filedata = data.get('data')

    if not filename or not filedata:
        print("[file_receiver] ❌ Invalid file data")
        return

    # Decode and preserve the content
    decoded_bytes = base64.b64decode(filedata)
    third_ans = decoded_bytes.decode('utf-8')  # Preserves formatting

    # Save the file
    os.makedirs("received_files", exist_ok=True)
    path = os.path.join("received_files", filename)
    with open(path, "wb") as f:
        f.write(decoded_bytes)

    print(f"[file_receiver] 📥 File saved as: {path}")
    print(f"[file_receiver] 📄 Extracted content stored in variable `third_ans`")
    
    # Optional: print preview
    print("\n----- FILE CONTENT BEGIN -----\n")
    print(third_ans)
    print("\n----- FILE CONTENT END -------\n")


def run_file_receiver():
    while True:
        try:
            print("[file_receiver] 🔄 Connecting...")
            sio.connect(CLOUD_URL, namespaces=[RECEIVE_NAMESPACE])
            sio.wait()
        except Exception as e:
            print("[file_receiver] ❌ Connection error:", e)
            time.sleep(5)
