from app.db.connection import get_db_connection

# --- Threads ---
def get_thread_id(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT thread_id FROM users WHERE user_id = %s', (user_id,))
    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]
    return None

def save_thread_id(user_id: int, thread_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO users (user_id, thread_id)
        VALUES (%s, %s)
        ON CONFLICT (user_id) DO UPDATE
        SET thread_id = EXCLUDED.thread_id
    ''', (user_id, thread_id))

    conn.commit()
    conn.close()