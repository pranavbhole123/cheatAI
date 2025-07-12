# keyboard_client.py

import keyboard                # pip install keyboard
import socketio                # pip install "python-socketio[client]"

HOST_IP = ""   # Example: 192.168.1.10
WS_URL = f"http://192.168.0.108:5050"
NAMESPACE = '/keyboard'

# Create Socket.IO client
sio = socketio.Client()

@sio.event(namespace=NAMESPACE)
def connect():
    print("[keyboard_client] ✅ Connected to keyboard relay server")

@sio.event(namespace=NAMESPACE)
def disconnect():
    print("[keyboard_client] ❌ Disconnected from server")

@sio.on('message', namespace=NAMESPACE)
def on_message(data):
    print(f"[keyboard_client] 📩 Received message: {data}")

def send(message):
    sio.emit('message', message, namespace=NAMESPACE)
    print(f"[keyboard_client] → Sent '{message}'")

def on_backtick(event):
    send("go")

def on_num(event):
    send("esc")

def on_f9(event):
    send("trigger")

def on_up(event):
    send("up")

def on_down(event):
    send("down")

if __name__ == "__main__":
    try:
        print(f"[keyboard_client] 🌐 Connecting to {WS_URL}{NAMESPACE}")
        sio.connect(WS_URL, namespaces=[NAMESPACE])

        keyboard.on_press_key("`", on_backtick)
        keyboard.on_press_key("num lock", on_num)
        keyboard.on_press_key("f9",on_f9)
        keyboard.on_press_key("up",on_up)
        keyboard.on_press_key("down",on_down)

        keyboard.wait()  # Keep process alive
    except KeyboardInterrupt:
        print("[keyboard_client] 🛑 Exiting...")
    finally:
        sio.disconnect()
