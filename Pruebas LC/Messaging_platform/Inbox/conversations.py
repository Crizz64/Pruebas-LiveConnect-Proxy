import sqlite3

DB_NAME = "database.db"

def get_conversations():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, canal, updated_at
        FROM conversations
        ORDER BY updated_at DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": r[0],
            "canal": r[1],
            "updated_at": r[2]
        }
        for r in rows
    ]
