import requests
from metodos.Token import obtener_token

def get_balance():
    token = obtener_token()
    headers = {"PageGearToken": token}

    res = requests.get(
        "https://api.liveconnect.chat/prod/proxy/balance",
        headers=headers
    )

    return res.json()
