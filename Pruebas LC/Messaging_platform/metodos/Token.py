import requests
import time

# =========================
# CONFIGURACIÓN DE CUENTAS
# =========================
# Idealmente esto debería venir de DB o variables de entorno
ACCOUNTS = {
    1: {
        "cKey": "TU_CKEY_1",
        "privateKey": "TU_SECRET_1"
    },
    # 2: {
    #     "cKey": "TU_CKEY_2",
    #     "privateKey": "TU_SECRET_2"
    # }
}

DEFAULT_IDC = 1

# =========================
# CACHE DE TOKENS
# =========================
TOKENS = {}
TOKEN_TTL = 28800 - 60  # 8 horas - 1 minuto

TOKEN_URL = "https://api.liveconnect.chat/prod/account/token"


def obtener_token(idc: int = None):
    """
    Retorna un PageGearToken válido para el IDC indicado.
    Si no se pasa IDC, usa el DEFAULT_IDC (compatibilidad).
    """
    if idc is None:
        idc = DEFAULT_IDC

    if idc not in ACCOUNTS:
        return {
            "ok": False,
            "error": f"No existe configuración para IDC {idc}"
        }

    now = time.time()
    cached = TOKENS.get(idc)

    # 🔁 Reutilizar token si aún es válido
    if cached and now < cached["expira"]:
        return {
            "ok": True,
            "token": cached["token"],
            "idc": idc,
            "cached": True
        }

    creds = ACCOUNTS[idc]

    try:
        res = requests.post(
            TOKEN_URL,
            json={
                "cKey": creds["cKey"],
                "privateKey": creds["privateKey"]
            },
            timeout=20
        )
    except requests.RequestException as e:
        return {"ok": False, "error": f"Error de red en token: {str(e)}"}

    try:
        payload = res.json()
    except ValueError:
        return {
            "ok": False,
            "error": "Respuesta inválida al generar token",
            "raw_response": res.text
        }

    if not res.ok or payload.get("status") != 1:
        return {
            "ok": False,
            "error": payload
        }

    token = payload.get("PageGearToken")
    data = payload.get("data", {})
    returned_idc = data.get("idc")

    # 🔒 Validación cruzada
    if str(returned_idc) != str(idc):
        return {
            "ok": False,
            "error": f"IDC mismatch: esperado {idc}, recibido {returned_idc}"
        }

    # 💾 Cachear token
    TOKENS[idc] = {
        "token": token,
        "expira": now + TOKEN_TTL
    }

    print(f"🔑 Token generado para IDC {idc}: {token[:18]}...")

    return {
        "ok": True,
        "token": token,
        "idc": idc,
        "cached": False
    }
