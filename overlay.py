import uuid
import time
import ctypes
import win32con
import win32gui
import win32api

overlay_text = ""
visible = False
scroll_offset = 0

VK_ESCAPE = win32con.VK_ESCAPE

def get_monospace_font(point_size=12):
    # 1) Get screen DPI (pixels per inch in Y)
    hdc = win32gui.GetDC(0)
    dpi = ctypes.windll.gdi32.GetDeviceCaps(hdc, win32con.LOGPIXELSY)
    win32gui.ReleaseDC(0, hdc)

    # 2) Convert point size to logical height (negative for character height)
    lfHeight = -int(point_size * dpi / 72)

    # 3) Fill a LOGFONT structure
    lf = win32gui.LOGFONT()
    lf.lfHeight         = lfHeight
    lf.lfWidth          = 0
    lf.lfEscapement     = 0
    lf.lfOrientation    = 0
    lf.lfWeight         = win32con.FW_NORMAL
    lf.lfItalic         = 0
    lf.lfUnderline      = 0
    lf.lfStrikeOut      = 0
    lf.lfCharSet        = win32con.ANSI_CHARSET
    lf.lfOutPrecision   = win32con.OUT_DEFAULT_PRECIS
    lf.lfClipPrecision  = win32con.CLIP_DEFAULT_PRECIS
    lf.lfQuality        = win32con.DEFAULT_QUALITY
    lf.lfPitchAndFamily = win32con.FIXED_PITCH | win32con.FF_MODERN
    lf.lfFaceName       = "Consolas"

    # 4) Create and return the HFONT
    return win32gui.CreateFontIndirect(lf)


def wnd_proc(hwnd, msg, wparam, lparam):
    global overlay_text, scroll_offset

    if msg == win32con.WM_PAINT:
        hdc, paintStruct = win32gui.BeginPaint(hwnd)

        # 1) Fill background
        brush = win32gui.GetStockObject(win32con.BLACK_BRUSH)
        win32gui.FillRect(hdc, win32gui.GetClientRect(hwnd), brush)

        # 2) Setup text colors and transparent background
        win32gui.SetTextColor(hdc, win32api.RGB(255, 255, 255))
        win32gui.SetBkMode(hdc, win32con.TRANSPARENT)

        # 3) Select a monospaced font
        font = get_monospace_font(12)   # tweak size if needed
        old_font = win32gui.SelectObject(hdc, font)

        if overlay_text:
            rect = win32gui.GetClientRect(hwnd)
            left, top, right, bottom = rect

            # 4) Split & window the lines
            lines = overlay_text.splitlines()
            visible_lines = lines[scroll_offset : ]

            # 5) Draw each line with padding & spacing
            padding_x, padding_y = 2, 10
            line_spacing = 4
            y = top + padding_y

            for line in visible_lines:
                win32gui.DrawText(
                    hdc,
                    line,
                    -1,
                    (left + padding_x, y, right, bottom),
                    win32con.DT_LEFT | win32con.DT_TOP | win32con.DT_SINGLELINE
                )
                _, line_h = win32gui.GetTextExtentPoint32(hdc, line)
                y += line_h + line_spacing

        # 6) Clean up
        win32gui.SelectObject(hdc, old_font)
        win32gui.DeleteObject(font)
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
    10, 10, 1300, 1000,
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
