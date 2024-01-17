import unittest
import numpy as np
import ee
from api_utils import *
ee.Initialize()

class ApiUtilsTest(unittest.TestCase):

    def test_array_to_rbga(self):
        arr = np.ones((10, 10, 3))
        result = array_to_rbga(arr)
        assert np.any(np.isnan(result)) == False
        assert result.shape[-1] == 4 
        assert len(result.shape) == 3 


    def test_lognormalise(self):
        arr = np.array([[1, 2, 3], [4, 5, 6]])
        result = lognormalise(arr)
        assert np.any(np.isnan(result)) == False


    def test_get_download_requests(self):
        params = {
            'roi': "-98.95,19.34,-98.94,19.35",
            'start_date': '2022-01-01',
            'end_date': '2022-07-31',
            'cloud_cover': 100,
            'image_type': 'Colour',
            'aggregation_type': 'median',
            'aggregation_length': 'monthly'
        }
        result = get_download_requests(params)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], str)

    def test_process_images(self):
        image_paths = ['testimg.tif']
        result = process_images(image_paths)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], str)

    def test_create_gif(self):
        params = {
            'roi': "-98.95,19.34,-98.94,19.35",
            'start_date': '2022-01-01',
            'end_date': '2022-07-31',
            'cloud_cover': 100,
            'image_type': 'Colour',
            'aggregation_type': 'median',
            'aggregation_length': 'monthly'
        }


        request = get_download_requests(params)
        urls = download_urls(request, 'downloads')

        image_paths = process_images(urls)

        result = create_gif(image_paths)
        self.assertIsInstance(result, str)

    def test_generate_statistics(self):
        image_paths = ['testimg.tif']
        result = generate_statistics(image_paths)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], dict)

    def test_handle_request(self):
        params = {
            'roi': "-98.95,19.34,-98.94,19.35",
            'start_date': '2022-01-01',
            'end_date': '2022-07-31',
            'cloud_cover': 100,
            'image_type': 'Colour',
            'aggregation_type': 'median',
            'aggregation_length': 'monthly'
        }
        result = handle_request(params)
        
        self.assertIsInstance(result, dict)
        self.assertIn('ImgUrls', result)
        self.assertIn('GifUrl', result)
        self.assertIn('Stats', result)

    def test_format_response(self):
        params = {
            'roi': "-98.95,19.34,-98.94,19.35",
            'start_date': '2022-01-01',
            'end_date': '2022-07-31',
            'cloud_cover': 100,
            'image_type': 'Colour',
            'aggregation_type': 'median',
            'aggregation_length': 'monthly'
        }
        response = handle_request(params)

        result = format_response(response)
        self.assertIsInstance(result, str)

if __name__ == '__main__':
    unittest.main()