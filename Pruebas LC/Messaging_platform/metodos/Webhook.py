from DB.database import get_db

def procesar_webhook(data):
    conv_id = data.get("id_conversacion")
    mensaje = data.get("mensaje", "")
    canal = data.get("canal", "unknown")

    conn = get_db()
    cursor = conn.cursor()

    # Insertar conversación si no existe
    cursor.execute("""
        INSERT OR IGNORE INTO conversations (id, canal)
        VALUES (?, ?)
    """, (conv_id, canal))

    # Insertar mensaje
    cursor.execute("""
        INSERT INTO messages (conversation_id, sender, message)
        VALUES (?, ?, ?)
    """, (conv_id, "usuario", mensaje))

    conn.commit()
    conn.close()

    return {"status": "ok"}
