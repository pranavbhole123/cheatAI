import cv2
import pyautogui
import pytesseract
import socketio
import win32gui
import threading
import time
import os
from dotenv import load_dotenv
import overlay
import websock
from openai_api import extract_image_o1, image_to_o1, question_to_o3
from datetime import datetime
from gemini_api import gemini
# Configure pytesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
NAMESPACE = '/keyboard'
# WebSocket client setup
load_dotenv()
sio = socketio.Client()
SERVER_URL = os.getenv("KEYBOARD_SERVER_URL")

# Initial placeholder answers
latest_o3 = "this is o3"
latest_4 = "this is gpt 4"
ans_gem = "this is gem"
state = 0

os.makedirs('query', exist_ok=True)
def screenchot():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = os.path.join("query", f"screenshot_{timestamp}.png")
    pyautogui.screenshot(filename)
    print(f"[Overlay] 📸 Saved screenshot as {filename}")

def ocr():
    image = cv2.imread("image1.png")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    cv2.imwrite("processed_image.png", thresh)
    text = pytesseract.image_to_string(thresh, config="--oem 1 --psm 6")
    print(text)
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(text)
    return text

def get_naswers():
    return [latest_o3,ans_gem,latest_4]

# WebSocket event handlers
@sio.on('go', namespace=NAMESPACE)
def on_go(data):
    global latest_o1, latest_o3
    print("[Overlay] Received: go")


    screenchot()
   
    overlay.toggle_overlay()

@sio.on('mcq' , namespace=NAMESPACE)
def on_mcq(data):
    global latest_o1
    text1 = "solve this mcq and give the answer as otion and reason in one line"
    latest_o1 = image_to_o1(text1)
    websock.send_screenshot()
    image_paths = []

    for filename in sorted(os.listdir("query")):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            path = os.path.join("query", filename)
            image_paths.append(path)
    for path in image_paths:
        try:
            os.remove(path)
        except Exception as e:
            print(f"⚠️ Failed to delete {path}: {e}")
    overlay.toggle_overlay()


@sio.on('trigger',namespace=NAMESPACE)
def on_trigger(data):
    global latest_o3,latest_4,ans_gem
    overlay.toggle_overlay()
    
    question = extract_image_o1()
    latest_o3 = question_to_o3(question,model_name="o3-mini-2025-01-31")
    latest_4 = question_to_o3(question,model_name="gpt-4.1-2025-04-14")
    ans_gem = gemini(question)
    overlay.toggle_overlay()



@sio.on('esc', namespace=NAMESPACE)
def on_esc(data):
    global state
    print("[Overlay] Received: esc")

    #websock.send_screenshot()
    overlay.toggle_overlay()

    if overlay.visible:
        temp = get_naswers()
        overlay.overlay_text = temp[state]
        state = (state + 1) % len(temp)

        win32gui.InvalidateRect(overlay.hwnd, None, True)
        win32gui.UpdateWindow(overlay.hwnd)

@sio.on('up',namespace=NAMESPACE)
def on_up(data):
    if overlay.visible:
        overlay.scroll_offset+=1
        win32gui.InvalidateRect(overlay.hwnd, None, True)
        win32gui.UpdateWindow(overlay.hwnd)

@sio.on('down',namespace=NAMESPACE)
def on_down(data):
    if overlay.visible:
        if overlay.scroll_offset>0:
            overlay.scroll_offset-=1
        win32gui.InvalidateRect(overlay.hwnd, None, True)
        win32gui.UpdateWindow(overlay.hwnd)

@sio.event( namespace=NAMESPACE)
def connect():
    print("[Overlay] ✅ Connected to WebSocket server")

@sio.event( namespace=NAMESPACE)
def disconnect():
    print("[Overlay] ❌ Disconnected from WebSocket server")

def start_overlay_client():
    while True:
        try:
            print(f"[Overlay WS] Connecting to {SERVER_URL}…")
            sio.connect(SERVER_URL)
            print("[Overlay WS] Connected, entering wait()")
            sio.wait()  # blocks until disconnected
            print("[Overlay WS] wait() returned, disconnected unexpectedly")
        except Exception as e:
            print(f"[Overlay WS] Connection error: {e}")
        # Sleep before retrying
        time.sleep(5)

if __name__ == "__main__":
    threading.Thread(target=start_overlay_client, daemon=True).start()
    threading.Thread(target=overlay.enforce_topmost, daemon=True).start()
    win32gui.PumpMessages()
