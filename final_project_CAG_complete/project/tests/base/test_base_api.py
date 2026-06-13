import json
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from backend.server import create_server


class BaseApiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = create_server(port=0)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def url(self, path):
        return f"http://127.0.0.1:{self.port}{path}"

    def get_json(self, path):
        with urlopen(self.url(path), timeout=5) as response:
            return response.status, json.loads(response.read().decode("utf-8"))

    def post_json(self, path, payload):
        request = Request(
            self.url(path),
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=5) as response:
            return response.status, json.loads(response.read().decode("utf-8"))

    def test_health_returns_ok(self):
        status, body = self.get_json("/health")

        self.assertEqual(status, 200)
        self.assertEqual(body["status"], "ok")

    def test_ask_answers_from_knowledge_base(self):
        status, body = self.post_json(
            "/api/ask",
            {"user_id": "base-user", "question": "Que es RAG en el curso?"},
        )

        self.assertEqual(status, 200)
        self.assertIn("RAG recupera", body["answer"])
        self.assertIn("rag", body["sources"])
        self.assertEqual(body["context_used"], [])

    def test_ask_requires_user_and_question(self):
        with self.assertRaises(HTTPError) as error:
            self.post_json("/api/ask", {"user_id": "base-user"})

        self.assertEqual(error.exception.code, 400)
        error.exception.close()


if __name__ == "__main__":
    unittest.main()
