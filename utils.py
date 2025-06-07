import cv2
import pyautogui
import pytesseract
from flask import Flask, request, jsonify
import win32gui
import websock
import overlay        # import the overlay module, not individual names
from openai_api import extract_image_o1, image_to_o1, question_to_o3

# Point pytesseract to your Tesseract install
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app = Flask(__name__)

# Initial placeholder answers
latest_o1 = "hello i am pranav"
latest_o3 = "hello i am parth"
answers = [latest_o1, latest_o3]
state = 0

def screenchot():
    pyautogui.screenshot("image1.png")

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

@app.route("/", methods=["POST"])
def receive():
    global latest_o1, latest_o3, state, answers

    data = request.get_json(force=True)
    msg = data.get("message", "").lower()

    if msg == "go":
        # Show overlay
        overlay.toggle_overlay()

        # Take screenshot and send to o1
        screenchot()
        latest_o1 = image_to_o1()

        #send the image to server(friend)
        #websocket.send_screenshot()


        # Extract question (either via OCR or via o1 extract)
        question = extract_image_o1()

        # Send question to o3
        latest_o3 = question_to_o3(question)

        # Update answers list so ESC cycles properly
        answers = [latest_o1, latest_o3]

        # Hide overlay
        overlay.toggle_overlay()

        return jsonify(status="ok", action="toggle"), 200

    elif msg == "esc":
        # Toggle overlay on if not already visible
        websock.send_screenshot()
        overlay.toggle_overlay()
        if overlay.visible:

        # Update the overlay text in the overlay module
            overlay.overlay_text = answers[state]
            state = (state + 1) % len(answers)

            # Force repaint of the overlay window
            win32gui.InvalidateRect(overlay.hwnd, None, True)
            win32gui.UpdateWindow(overlay.hwnd)

        return jsonify(status="ok", action="exit"), 200

    else:
        return jsonify(status="error", error="Unknown message"), 400

def run_flask():
    app.run(host="0.0.0.0", port=8000, threaded=True)

if __name__ == "__main__":
    # Start Flask in a thread
    import threading
    threading.Thread(target=run_flask, daemon=True).start()

    # Start the overlay's topmost enforcer
    threading.Thread(target=overlay.enforce_topmost, daemon=True).start()

    # Enter the Win32 message loop
    win32gui.PumpMessages()
