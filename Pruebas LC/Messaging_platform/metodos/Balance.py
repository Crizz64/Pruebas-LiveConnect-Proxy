import requests
from metodos.Token import obtener_token
from DB.database import save_balance

BALANCE_URL = "https://api.liveconnect.chat/prod/proxy/balance"


def get_balance(idc: int = None):
    """
    Consulta el balance de la cuenta indicada por IDC.
    Si no se pasa IDC, usa la cuenta por defecto.
    """

    # 🔑 Obtener token por cuenta
    token_data = obtener_token(idc)
    if not token_data.get("ok"):
        return token_data

    token = token_data["token"]
    expected_idc = token_data["idc"]

    headers = {
        "Accept": "application/json",
        "PageGearToken": token
    }

    try:
        res = requests.get(
            BALANCE_URL,
            headers=headers,
            timeout=20
        )
    except requests.RequestException as e:
        return {
            "ok": False,
            "error": f"Error de red en balance: {str(e)}"
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

    data = payload.get("data")
    if not isinstance(data, dict):
        return {
            "ok": False,
            "error": "No se encontró data válida en la respuesta",
            "payload": payload
        }

    received_idc = data.get("idc")

    # 🔒 Validación de seguridad
    if str(received_idc) != str(expected_idc):
        return {
            "ok": False,
            "error": f"IDC mismatch: esperado {expected_idc}, recibido {received_idc}"
        }

    result = {
        "ok": True,
        "idc": received_idc,
        "balance": data.get("balance"),
        "channels": {
            "web": data.get("web", 0),
            "insta": data.get("insta", 0),
            "wapi": data.get("wapi", 0),
            "wabags": data.get("wabags", 0),
            "messenger": data.get("messenger", 0),
        },
        "detail": data
    }

    # 💾 Guardar balance por cuenta
    save_balance(result)

    return result
