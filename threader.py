import threading
import win32gui
import utils
import overlay
import websock
import file_reciever_sock

if __name__ == "__main__":
    threading.Thread(target=overlay.enforce_topmost, daemon=True).start()
    threading.Thread(target=utils.run_flask, daemon=True).start()
    threading.Thread(target=websock.run_ws, daemon=True).start()
    threading.Thread(target=file_reciever_sock.run_file_receiver, daemon=True).start()  # Receives file from /recieve_file


    win32gui.PumpMessages()
