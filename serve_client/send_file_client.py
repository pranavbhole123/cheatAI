# send_file_client.py
import socketio
import base64
import os
import time

CLOUD_URL = 'http://34.131.212.123:5000'
NAMESPACE = '/send_file'

# Create a Socket.IO client
sio = socketio.Client()

@sio.event(namespace=NAMESPACE)
def connect():
    print(f"🔌 Connected to {CLOUD_URL} on namespace {NAMESPACE}")
    print("📂 Ready to send a file. Enter the full path of the file below:")

@sio.event(namespace=NAMESPACE)
def disconnect():
    print("🔌 Disconnected from server")

@sio.on('ack', namespace=NAMESPACE)
def on_ack(data):
    print("✅ Server ACK:", data['message'])

@sio.on('received', namespace=NAMESPACE)
def on_received(data):
    print("📬 Server Response:", data['message'])

@sio.on('error', namespace=NAMESPACE)
def on_error(data):
    print("❌ Server Error:", data['message'])


def send_file(filepath):
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return

    filename = os.path.basename(filepath)
    with open(filepath, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('utf-8')

    sio.emit('file_upload', {
        'filename': filename,
        'data': b64
    }, namespace=NAMESPACE)
    print(f"📤 Sent file: {filename}")


def main():
    try:
        print("🔄 Connecting...")
        sio.connect(CLOUD_URL, namespaces=[NAMESPACE])
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return

    while True:
        try:
            filepath = input("📎 Enter file path to send (or 'exit' to quit): ").strip()
            if filepath.lower() == 'exit':
                break
            if filepath:
                send_file(filepath)
        except KeyboardInterrupt:
            break

    sio.disconnect()

if __name__ == "__main__":
    main()
