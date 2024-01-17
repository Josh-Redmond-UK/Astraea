import ee
import unittest
import os
from download_utils import *

class DownloadUtilsTest(unittest.TestCase):

    def setUp(self):
        # Initialize Earth Engine
        ee.Initialize()

    def test_get_download_jobs(self):
        roi  = ee.Geometry.Rectangle([-98.95, 19.34, -98.94, 19.35])
        image_collection = ee.ImageCollection('COPERNICUS/S2_SR').filterBounds(roi).filterDate('2022-01-01', '2022-01-31').select(['B3', 'B4', 'B8']).map(lambda image: image.clip(roi))

        # Get the download jobs
        result = get_download_jobs(image_collection)

        # Check if the result is a list
        self.assertIsInstance(result, list)

        # Check if the result contains strings
        for job in result:
            self.assertIsInstance(job, str)

    def test_download_image(self):
        # Define a sample image URL and path
        image_url = "https://picsum.photos/200/300.jpg"
        path = "image.jpg"

        # Download the image
        result = download_image(image_url, path)

        # Check if the result is the expected path
        self.assertEqual(result, path)

        # Check if the image file exists
        self.assertTrue(os.path.exists(path))

        # Clean up the downloaded image
        os.remove(path)


    def test_download_urls(self):
        # Define a sample URL list and folder path
        url_list = ["https://picsum.photos/200.jpg", "https://picsum.photos/200/300.jpg"]
        folder_path = "path/to/save/"

        # Download the URLs
        result = download_urls(url_list, folder_path)

        # Check if the result is a list
        self.assertIsInstance(result, list)

        # Check if the result contains the expected file paths
        expected_paths = [os.path.join(folder_path, f'image_{idx}.jpg') for idx in range(len(url_list))]
        self.assertEqual(result, expected_paths)

        # Check if the image files exist
        for path in expected_paths:
            self.assertTrue(os.path.exists(path))

            # Clean up the downloaded images
            os.remove(path)


        
if __name__ == '__main__':
    unittest.main()