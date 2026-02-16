import requests
from metodos.Token import obtener_token

GET_WEBHOOK_URL = "https://api.liveconnect.chat/prod/proxy/getWebhook"


def get_webhook(id_canal: int, idc: int = None):
    """
    Consulta la configuración de webhook de un canal
    para la cuenta indicada por IDC.
    """

    if not id_canal:
        return {
            "ok": False,
            "error": "id_canal es requerido"
        }

    # 🔑 Obtener token por cuenta
    token_data = obtener_token(idc)
    if not token_data.get("ok"):
        return token_data

    token = token_data["token"]
    account_idc = token_data["idc"]

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "PageGearToken": token
    }

    try:
        res = requests.post(
            GET_WEBHOOK_URL,
            json={"id_canal": id_canal},
            headers=headers,
            timeout=20
        )
    except requests.RequestException as e:
        return {
            "ok": False,
            "error": f"Error de red en getWebhook: {str(e)}"
        }

    try:
        payload = res.json()
    except ValueError:
        return {
            "ok": False,
            "error": "Respuesta inválida del servidor",
            "raw_response": res.text
        }

    if not res.ok or payload.get("status") != 1:
        return {
            "ok": False,
            "status_code": res.status_code,
            "error": payload
        }

    result = {
        "ok": True,
        "idc": account_idc,
        "id_canal": id_canal,
        "data": payload.get("data"),
        "detail": payload
    }

    return result
