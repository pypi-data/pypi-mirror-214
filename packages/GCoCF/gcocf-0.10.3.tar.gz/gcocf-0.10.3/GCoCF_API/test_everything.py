import unittest

from fastapi.testclient import TestClient
from service_api import app

client = TestClient(app)


class TestAPI(unittest.TestCase):
    def test_root(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Hello World"})

    def test_greet(self):
        response = client.get("/greet/TestUser")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Hello, TestUser"})


if __name__ == "__main__":
    unittest.main()
