import requests
import time
import threading

# ========================
# CONFIG
# ========================

KEY = ""
SECRET = ""
TOKEN_URL = "https://api.liveconnect.chat/prod/account/token"

# ========================
# CACHE
# ========================

_TOKEN_CACHE = {}
_LOCK = threading.Lock()

# ========================
# TOKEN HANDLER
# ========================

def obtener_token(force_refresh=False):
    """
    Obtiene y cachea el PageGearToken por KEY.
    """
    global _TOKEN_CACHE

    now = time.time()

    with _LOCK:
        cached = _TOKEN_CACHE.get(KEY)

        # Reutilizar token válido
        if (
            not force_refresh
            and cached
            and cached.get("token")
            and now < cached.get("expires", 0)
        ):
            return cached["token"]

        # Solicitar token nuevo
        response = requests.post(
            TOKEN_URL,
            json={"cKey": KEY, "privateKey": SECRET},
            timeout=15
        )

        if not response.ok:
            raise RuntimeError(
                f"Error obteniendo token ({response.status_code}): {response.text}"
            )

        data = response.json()
        token = data.get("PageGearToken")

        if not token:
            raise RuntimeError("Respuesta inválida: PageGearToken no presente")

        # Expiración segura (8h - 2 min)
        expires = now + (8 * 60 * 60) - 120

        _TOKEN_CACHE[KEY] = {
            "token": token,
            "expires": expires
        }

        print(f"🔑 Token generado para KEY {KEY[:6]}…")

        return token
