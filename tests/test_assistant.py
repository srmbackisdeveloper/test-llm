import unittest
from unittest.mock import patch
from llm.assistant import get_assistant_response

class TestAssistant(unittest.TestCase):

    @patch("app.llm.assistant.OpenAI")
    def test_get_assistant_response(self, mock_openai):
        mock_client = mock_openai.return_value
        mock_thread = mock_client.beta.threads.create.return_value
        mock_thread.id = "mock_thread_id"

        mock_run = mock_client.beta.threads.runs.create_and_poll.return_value
        mock_run.status = "completed"

        mock_messages = mock_client.beta.threads.messages.list.return_value
        mock_messages.data = [{"content": [{"text": {"value": "Test response"}}]}]

        response = get_assistant_response("test_user", "Hello!")
        self.assertEqual(response, "Test response")

if __name__ == "__main__":
    unittest.main()
