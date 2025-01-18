import unittest
from app.db.connection import get_db_connection, init_db

class TestDBConnection(unittest.TestCase):

    def test_get_db_connection(self):
        conn = get_db_connection()
        self.assertIsNotNone(conn)
        conn.close()

    def test_init_db(self):
        try:
            init_db()
        except Exception as e:
            self.fail(f"init_db error: {e}")

if __name__ == "__main__":
    unittest.main()
