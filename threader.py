import threading
import win32gui
import utils
import overlay

if __name__ == "__main__":
    threading.Thread(target=overlay.enforce_topmost, daemon=True).start()
    threading.Thread(target=utils.run_flask, daemon=True).start()
    win32gui.PumpMessages()
