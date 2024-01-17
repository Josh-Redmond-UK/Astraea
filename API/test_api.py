import unittest
import numpy as np
import ee
from main import app
from fastapi.testclient import TestClient
import json
ee.Initialize()

client = TestClient(app)

class ApiTest(unittest.TestCase):
    def test_app(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"Hello": "World"}

    def test_generate_maps(self):
        test_request_string = json.dumps({"roi":"-98.95,19.34,-98.94,19.35","start_date":"2022-01-01","end_date":"2022-07-31","cloud_cover":100,"image_type":"Colour","aggregation_type":"median","aggregation_length":"monthly"})
        response = client.get("/api/mapping", params={'params':test_request_string})
        print(response.json())
        assert response.status_code == 200


if __name__ == '__main__':
    unittest.main()
