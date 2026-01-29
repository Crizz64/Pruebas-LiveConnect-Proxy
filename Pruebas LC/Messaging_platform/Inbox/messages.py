import sqlite3

DB_NAME = "database.db"

def get_messages(conversation_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT sender, message, created_at
        FROM messages
        WHERE conversation_id = ?
        ORDER BY created_at ASC
    """, (conversation_id,))

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "sender": r[0],
            "message": r[1],
            "created_at": r[2]
        }
        for r in rows
    ]
