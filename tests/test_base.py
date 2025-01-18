import unittest
from fastapi.testclient import TestClient
from app.base import app

client = TestClient(app)

class TestBaseEndpoints(unittest.TestCase):

    def test_webhook_endpoint(self):
        payload = {"message": "Hello!", "callback_url": "http://localhost:8000/callback"}
        response = client.post("/webhook", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "processing")

    def test_callback_endpoint(self):
        payload = {"data": {"message": "Test callback"}}
        response = client.post("/callback", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "received")

    def test_get_messages_not_found(self):
        response = client.get("/messages", params={"user_id": "unknown_user"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "user not found.")

if __name__ == "__main__":
    unittest.main()
