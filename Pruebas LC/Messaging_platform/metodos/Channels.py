import requests
from metodos.Token import obtener_token

CHANNELS_URL = "https://api.liveconnect.chat/prod/channels/list"


def get_channels(idc: int = None, filters: dict | None = None):
    """
    Lista los canales de la cuenta indicada por IDC.
    Permite filtros opcionales (visible, estado, tipo, etc).
    """

    # 🔑 Obtener token por cuenta
    token_data = obtener_token(idc)
    if not token_data.get("ok"):
        return token_data

    token = token_data["token"]
    account_idc = token_data["idc"]

    headers = {
        "Accept": "application/json",
        "PageGearToken": token
    }

    # 🧹 Limpiar filtros vacíos
    clean_filters = {}
    if isinstance(filters, dict):
        for key, value in filters.items():
            if value is not None and str(value).strip() != "":
                clean_filters[key] = value

    try:
        res = requests.get(
            CHANNELS_URL,
            headers=headers,
            params=clean_filters,
            timeout=20
        )
    except requests.RequestException as e:
        return {
            "ok": False,
            "error": f"Error de red en channels/list: {str(e)}"
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

    result = {
        "ok": True,
        "idc": account_idc,
        "data": data,
        "filters": clean_filters
    }

    return result
