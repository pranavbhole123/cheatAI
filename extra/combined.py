import uuid
import threading
import time
import ctypes

import win32con
import win32gui
import win32api
from dotenv     import load_dotenv

import numpy as np
import cv2
import pyautogui
import base64
from openai import OpenAI
import os
import cv2
from PIL import Image
import pytesseract

from flask import Flask, request, jsonify


load_dotenv()

latest_o1 ="hello i am pranv i am very good "
latest_o3 = "hello i am parth i am excellent and very bright"
overlay_text = ""
state = 0
answers = [latest_o1,latest_o3]

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


VK_ESCAPE = win32con.VK_ESCAPE


def wnd_proc(hwnd, msg, wparam, lparam):
    global overlay_text

    if msg == win32con.WM_PAINT:
        hdc, paintStruct = win32gui.BeginPaint(hwnd)

        
        brush = win32gui.GetStockObject(win32con.BLACK_BRUSH)
        win32gui.FillRect(hdc, win32gui.GetClientRect(hwnd), brush)

        win32gui.SetTextColor(hdc, win32api.RGB(255, 255, 255))
        win32gui.SetBkMode(hdc, win32con.TRANSPARENT)

        if overlay_text:
            rect = win32gui.GetClientRect(hwnd)
            x, y = rect[0], rect[1]
            for line in overlay_text.splitlines():
                win32gui.DrawText(
                    hdc,
                    line,
                    -1,
                    (x, y, rect[2], rect[3]),
                    win32con.DT_LEFT | win32con.DT_TOP
                )
                (line_w, line_h) = win32gui.GetTextExtentPoint32(hdc, line)
                y += line_h

        win32gui.EndPaint(hwnd, paintStruct)
        return 0

    elif msg == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)
        return 0

    return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

# Register window class
# Register window class
wc = win32gui.WNDCLASS()
hinst = win32api.GetModuleHandle(None)
wc.hInstance = hinst
wc.lpszClassName = str(uuid.uuid4())
wc.lpfnWndProc = wnd_proc

# ← Add this line so that the client area is cleared to transparent before each paint
#wc.hbrBackground = win32gui.GetStockObject(win32con.NULL_BRUSH)

class_atom = win32gui.RegisterClass(wc)

# Create window
EX_STYLE = (
    win32con.WS_EX_LAYERED |
    win32con.WS_EX_TRANSPARENT |
    win32con.WS_EX_NOACTIVATE |
    win32con.WS_EX_TOPMOST
)
hwnd = win32gui.CreateWindowEx(
    EX_STYLE,
    class_atom,
    None,
    win32con.WS_POPUP,
    100, 100, 800, 800,
    None, None, hinst, None
)

# Set transparency and initial state
win32gui.SetLayeredWindowAttributes(hwnd, 0, 128, win32con.LWA_ALPHA)
win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
visible = False

def enforce_topmost():
    while True:
        if visible:
            ctypes.windll.user32.SetWindowPos(
                hwnd,
                win32con.HWND_TOPMOST,
                0, 0, 0, 0,
                win32con.SWP_NOMOVE |
                win32con.SWP_NOSIZE |
                win32con.SWP_FRAMECHANGED
            )
        time.sleep(0.5)

def toggle_overlay():
    global visible
    visible = not visible
    win32gui.ShowWindow(hwnd, win32con.SW_SHOW if visible else win32con.SW_HIDE)


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def extract_image_o1():
    image_path = "image1.png"

    base64_image = encode_image(image_path)

    response = client.responses.create(
        model="o1-2024-12-17",
        input=[
        {
            "role": "user",
            "content": [
                { "type": "input_text", "text": "extract all the details related to the coding question in the image in a nice format" },
                {
                    "type": "input_image",
                    "image_url": f"data:image/jpeg;base64,{base64_image}",
                },
            ],
        }
        ],
        )
    print("+++++++++++++++++++++++++++++++response form 01+++++++++++++++++++++++++++")
    print(response.output_text)
    return response.output_text

def ocr():
    image_path = "image1.png"
    image = cv2.imread(image_path)

    # Preprocessing: convert to grayscale and apply thresholding
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Save preprocessed image (optional)
    cv2.imwrite("processed_image.png", thresh)

    # OCR: extract text
    text = pytesseract.image_to_string(thresh, config="--oem 1 --psm 6")

    # Print or save result
    print("\n--- Extracted Text ---\n")
    print(text)

    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(text)
    return text


def screenchot():
    image = pyautogui.screenshot()
    image1 = pyautogui.screenshot("image1.png")

def image_to_o1():
    image_path = "image1.png"

    base64_image = encode_image(image_path)

    response = client.responses.create(
        model="o1-2024-12-17",
        input=[
        {
            "role": "user",
            "content": [
                { "type": "input_text", "text": "solve the coding question in this image in python" },
                {
                    "type": "input_image",
                    "image_url": f"data:image/jpeg;base64,{base64_image}",
                },
            ],
        }
        ],
        )
    print("+++++++++++++++++++++++++++++++response form 01+++++++++++++++++++++++++++")
    print(response.output_text)
    return response.output_text

def question_to_o3(question):
    model_name = 'o3-mini-2025-01-31'
    messages = [
        {"role": "system", "content": "Solve this coding problem and provide the answer in Python."},
        {"role": "user", "content": question}
    ]
    resp = client.chat.completions.create(
        model=model_name,
        messages=messages,
        reasoning_effort="high"
    )
    print("**************************response from 03*********************************")
    print(resp.choices[0].message.content)
    return resp.choices[0].message.content


    

app = Flask(__name__)

@app.route("/", methods=["POST"])
def receive():
    global latest_o1,latest_o3
    data = request.get_json(force=True)
    msg = data.get("message", "").lower()

    if msg == "go":
        toggle_overlay()
        
        screenchot()
        latest_o1 = image_to_o1()

        #question = ocr()
        question = extract_image_o1()
        #now we need to call ocr to extract text and give it to the o3

        latest_o3 = question_to_o3(question)

        toggle_overlay()


        return jsonify(status="ok", action="toggle"), 200
    
    elif msg == "esc":
        global overlay_text,answers,state
        
        toggle_overlay()
        if visible:
            overlay_text = answers[state]
            print(overlay_text)
            state+=1
            state = state % len(answers)
            #print(latest_o1)
            # Force a WM_PAINT so the new overlay_text is drawn immediately
            win32gui.InvalidateRect(hwnd, None, True)
            win32gui.UpdateWindow(hwnd)

        
        return jsonify(status="ok", action="exit"), 200
    else:
        return jsonify(status="error", error="Unknown message"), 400

def run_flask():
    # Note: threaded=True allows Flask to handle multiple requests if needed.
    app.run(host="0.0.0.0", port=8000, threaded=True)



if __name__ == "__main__":
    # Start the thread that keeps the overlay on top
    threading.Thread(target=enforce_topmost, daemon=True).start()

    # Start Flask in a separate daemon thread
    threading.Thread(target=run_flask, daemon=True).start()

    # Enter the Win32 message loop (blocks here)
    win32gui.PumpMessages()
