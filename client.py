import keyboard    # pip install keyboard
import requests    # pip install requests
import sys

HOST_IP = "192.168.0.119"   # ← change to your host’s IP as seen from the VM
URL = f"http://{HOST_IP}:8000/"

def send(message):
    try:
        resp = requests.post(URL, json={"message": message}, timeout=15)
        print(f"→ Sent '{message}', Response:", resp.json())
    except Exception as e:
        print("Error:", e)

def on_backtick(event):
    send("go")

def on_esc(event):
    send("esc")

if __name__ == "__main__":
    #print("Press ` to send 'go' message to server.")
    #print("Press Esc to send 'esc' message to server.")
    
    keyboard.on_press_key("`", on_backtick)
    keyboard.on_press_key("esc", on_esc)

    keyboard.wait()  # Blocks until interrupted (e.g. Ctrl+C)