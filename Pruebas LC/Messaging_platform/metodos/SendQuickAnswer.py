import requests
from metodos.Token import obtener_token

def send_quick_answer(data):
    token = obtener_token()
    headers = {
        "Content-Type": "application/json",
        "PageGearToken": token
    }

    res = requests.post(
        "https://api.liveconnect.chat/prod/proxy/sendQuickAnswer",
        json=data,
        headers=headers
    )

    return res.json()
