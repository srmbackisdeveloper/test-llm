from app.db.connection import get_db_connection
from datetime import datetime
import json

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

# --- Messages ---
def save_message(user_id: str, role: str, content: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Define the new message as a JSON object
    new_message = {
        "role": role,
        "time": datetime.now().isoformat(),
        "message": content
    }

    # Update the messages column by appending the new message to the JSON array
    cursor.execute('''
    INSERT INTO users (user_id, messages)
    VALUES (%s, %s)
    ON CONFLICT (user_id) DO UPDATE
    SET messages = users.messages || %s::jsonb
    ''', (user_id, json.dumps([new_message]), json.dumps(new_message)))

    conn.commit()
    conn.close()


def get_messages(user_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
    SELECT messages FROM users
    WHERE user_id = %s
    ''', (user_id,))

    result = cursor.fetchone()
    conn.close()

    return result[0] if result else []