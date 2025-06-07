import uuid
import threading
import time
import ctypes

import win32con
import win32gui
import win32api
import keyboard  # <-- Global keyboard hook

VK_ESCAPE = win32con.VK_ESCAPE

def wnd_proc(hwnd, msg, wparam, lparam):
    if msg == win32con.WM_PAINT:
        hdc = win32gui.GetDC(hwnd)
        win32gui.SetTextColor(hdc, win32api.RGB(255, 255, 255))
        win32gui.SetBkMode(hdc, win32con.TRANSPARENT)
        win32gui.DrawText(hdc, "Hello World", -1,
                          win32gui.GetClientRect(hwnd),
                          win32con.DT_LEFT | win32con.DT_TOP)
        win32gui.ReleaseDC(hwnd, hdc)
        return 0
    elif msg == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)
        return 0
    return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

# Register window class
wc = win32gui.WNDCLASS()
hinst = win32api.GetModuleHandle(None)
wc.hInstance = hinst
wc.lpszClassName = str(uuid.uuid4())
wc.lpfnWndProc = wnd_proc
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
    100, 100, 400, 300,
    None, None, hinst, None
)

# Set transparency
win32gui.SetLayeredWindowAttributes(hwnd, 0, 128, win32con.LWA_ALPHA)
win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
visible = False

# Keep topmost
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

# Toggle overlay visibility
def toggle_overlay():
    global visible
    visible = not visible
    win32gui.ShowWindow(hwnd, win32con.SW_SHOW if visible else win32con.SW_HIDE)

# Handle ESC and backtick globally
def global_keys():
    keyboard.add_hotkey('`', toggle_overlay)
    keyboard.add_hotkey('esc', lambda: win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0))
    keyboard.wait()  # Block forever

# Start threads
threading.Thread(target=global_keys, daemon=True).start()
threading.Thread(target=enforce_topmost, daemon=True).start()

# Message loop
win32gui.PumpMessages()
