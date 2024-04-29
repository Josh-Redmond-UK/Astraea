import unittest
import numpy as np
import ee
from main import app
from fastapi.testclient import TestClient
import json
import requests
ee.Authenticate()
ee.Initialize()

client = TestClient(app)

class ApiTest(unittest.TestCase):
    def test_app(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"Hello": "World"}

    def test_generate_maps(self):
        test_request_string = json.dumps({"roi":"-98.95,19.34,-98.94,19.35","startDate":"2022-01-01","endDate":"2022-07-31","cloudCover":100,"imageMode":"Colour","aggType":"median","aggLength":"monthly"})
        print("JSON REQUEST:", test_request_string)
        response = client.get("/api/mapping", params={'params':test_request_string})
        print(response.json())
        assert response.status_code == 202

    def test_handling_text_query(self):
        roi = "-98.95,19.34,-98.94,19.35"
        start_date = "2022-01-01"
        end_date = "2022-07-31"
        cloud_cover = 100
        image_type = "Colour"
        aggregation_type = "median"
        aggregation_length = "monthly"
        test_request = json.dumps({"roi":roi, "startDate":start_date, "endDate":end_date, "cloudCover":cloud_cover, "imageMode":image_type, "aggType":aggregation_type, "aggLength":aggregation_length})
        print("FORMATTED REQUEST STRING", test_request)
        #test_string = f"roi=${drawingData.points}&cloud_cover=100&start_date=${drawingData.startDate}&end_date=${drawingData.endDate}&image_type=${drawingData.imageMode}&aggregation_length=${drawingData.aggLenth}&aggregation_type=${drawingData.aggType}`;"
        response = client.get("/api/mapping", params={"params":test_request})
        print(response.json())
        print(response.status_code)
        assert response.status_code == 202


if __name__ == '__main__':
    unittest.main()
