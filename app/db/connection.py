import psycopg2
from app.settings import DSN

def get_db_connection():
    return psycopg2.connect(dsn=DSN)

def init_db():
    conn = get_db_connection()
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        thread_id TEXT
    )
    ''')

    conn.commit()
    conn.close()