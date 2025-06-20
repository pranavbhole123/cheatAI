import uuid
import time
import ctypes
import win32con
import win32gui
import win32api

overlay_text = ""
visible = False

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
                win32gui.DrawText(hdc, line, -1, (x, y, rect[2], rect[3]), win32con.DT_LEFT | win32con.DT_TOP)
                (line_w, line_h) = win32gui.GetTextExtentPoint32(hdc, line)
                y += line_h
        win32gui.EndPaint(hwnd, paintStruct)
        return 0

    elif msg == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)
        return 0

    return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

wc = win32gui.WNDCLASS()
hinst = win32api.GetModuleHandle(None)
wc.hInstance = hinst
wc.lpszClassName = str(uuid.uuid4())
wc.lpfnWndProc = wnd_proc
class_atom = win32gui.RegisterClass(wc)

EX_STYLE = (
    win32con.WS_EX_LAYERED |
    win32con.WS_EX_TRANSPARENT |
    win32con.WS_EX_NOACTIVATE |
    win32con.WS_EX_TOPMOST
)

hwnd = win32gui.CreateWindowEx(
    EX_STYLE, class_atom, None, win32con.WS_POPUP,
    10, 10, 1000, 1000,
    None, None, hinst, None
)

win32gui.SetLayeredWindowAttributes(hwnd, 0, 200, win32con.LWA_ALPHA)
win32gui.ShowWindow(hwnd, win32con.SW_HIDE)


def toggle_overlay():
    global visible
    visible = not visible
    win32gui.ShowWindow(hwnd, win32con.SW_SHOW if visible else win32con.SW_HIDE)

def enforce_topmost():
    while True:
        if visible:
            ctypes.windll.user32.SetWindowPos(
                hwnd, win32con.HWND_TOPMOST,
                0, 0, 0, 0,
                win32con.SWP_NOMOVE |
                win32con.SWP_NOSIZE |
                win32con.SWP_FRAMECHANGED
            )
        time.sleep(0.5)
