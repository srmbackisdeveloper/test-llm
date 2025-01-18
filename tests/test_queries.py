import unittest
from app.db.queries import save_message, get_messages, get_thread_id, save_thread_id
from app.db.connection import init_db, get_db_connection

class TestQueries(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        init_db()

    def test_save_thread_id_and_get_thread_id(self):
        user_id = "test_user"
        thread_id = "test_thread"
        save_thread_id(user_id, thread_id)
        retrieved_thread_id = get_thread_id(user_id)
        self.assertEqual(retrieved_thread_id, thread_id)

    def test_save_message_and_get_messages(self):
        user_id = "test_user"
        save_message(user_id, "user", "Hello!")
        messages = get_messages(user_id)
        self.assertTrue(len(messages) > 0)
        self.assertEqual(messages[0]["message"], "Hello!")

if __name__ == "__main__":
    unittest.main()
