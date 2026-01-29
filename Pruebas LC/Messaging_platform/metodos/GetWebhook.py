import requests
from metodos.Token import obtener_token
def get_webhook(id_canal):
    token = obtener_token()
    headers = {
        "Content-Type": "application/json",
        "PageGearToken": token
    }

    res = requests.post(
        "https://api.liveconnect.chat/prod/proxy/getWebhook",
        json={"id_canal": id_canal},
        headers=headers
    )

    return res.json()
