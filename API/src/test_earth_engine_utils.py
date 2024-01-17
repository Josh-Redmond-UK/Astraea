import ee
import unittest
from earth_engine_utils import *

class EarthEngineUtilsTest(unittest.TestCase):

    def setUp(self):
        # Initialize Earth Engine
        ee.Initialize()

    def test_get_BAIS2(self):
        # Create a sample image
        image = ee.ImageCollection('COPERNICUS/S2_SR').first()

        # Calculate BAIS2 index
        result = get_BAIS2(image)

        # Check if the result is an ee.Image
        self.assertIsInstance(result, ee.Image)

        # Check if image is valid
        result.getInfo()

    def test_get_NBR(self):
        # Create a sample image
        image = ee.ImageCollection('COPERNICUS/S2_SR').first()
        
        # Calculate NBR index
        result = get_NBR(image)

        # Check if the result is an ee.Image
        self.assertIsInstance(result, ee.Image)

        # Check if image is valid
        result.getInfo()

    def test_get_NDVI(self):
        # Create a sample image
        image = ee.ImageCollection('COPERNICUS/S2_SR').first()
        
        # Calculate NDVI index
        result = get_NDVI(image)

        # Check if the result is an ee.Image
        self.assertIsInstance(result, ee.Image)

        # Check if image is valid
        result.getInfo()


    def test_get_spectral_index(self):
        roi  = ee.Geometry.Rectangle([-98.95, 19.34, -98.94, 19.35])

        image_collection = ee.ImageCollection('COPERNICUS/S2_SR').filterBounds(roi).filterDate('2022-01-01', '2022-01-31')

        ndvi = get_spectral_index(image_collection, 'NDVI')
        ndvi.getInfo()
        nbr = get_spectral_index(image_collection, 'NBR')
        nbr.getInfo()
        bais2 = get_spectral_index(image_collection, 'BAIS2')
        bais2.getInfo()
        colour = get_spectral_index(image_collection, 'Colour')
        colour.getInfo()


    def test_get_images_for_extent(self):
        # Create a sample region of interest
        roi  = ee.Geometry.Rectangle([-98.95, 19.34, -98.94, 19.35])

        # Set the start and end dates
        start_date = '2022-01-01'
        end_date = '2022-01-31'

        # Set the maximum cloud cover
        cloud_cover = 10

        # Calculate NDVI index for the specified extent
        result = get_images_for_extent(roi, start_date, end_date, cloud_cover, 'NDVI')

        # Check if the result is an ee.ImageCollection
        self.assertIsInstance(result, ee.ImageCollection)

    def test_aggregate_collection(self):
        # Create a sample image collection
        roi  = ee.Geometry.Rectangle([-98.95, 19.34, -98.94, 19.35])

        # Set the aggregation type, length, start date, and end date
        aggregation_type = 'mean'
        aggregation_length = 'monthly'
        start_date = '2021-01-01'
        end_date = '2021-12-31'

        image_collection = ee.ImageCollection('COPERNICUS/S2_SR').filterBounds(roi).filterDate(start_date, end_date)


        # Aggregate the image collection
        result = aggregate_collection(image_collection, aggregation_type, aggregation_length, start_date, end_date)
        
        # Check if the result is an ee.ImageCollection
        self.assertIsInstance(result, ee.ImageCollection)

        # Check if image is valid
        result.first().projection().nominalScale().getInfo()

    def test_numberOfPixels(self):
        # Create a sample image
        image = ee.ImageCollection('COPERNICUS/S2_SR').first()

        # Calculate the number of pixels
        result = numberOfPixels(image)

        # Check if the result is a tuple of ee.Number
        self.assertIsInstance(result, tuple)
        self.assertIsInstance(result[0], ee.Number)
        self.assertIsInstance(result[1], ee.Number)

    def test_convert_projection_resolution(self):
        # Create a sample image
        image = ee.ImageCollection('COPERNICUS/S2_SR').first().select(['B4', 'B3', 'B2'])

        # Set the target size
        target_size = 100

        # Convert the projection resolution
        result = convert_projection_resolution(image, target_size)

        # Check if the result is an ee.Projection
        self.assertIsInstance(result, ee.Projection)

        # Check if projection is valid
        result.getInfo()

    def test_scale_image(self):
        # Create a sample image
        image = ee.ImageCollection('COPERNICUS/S2_SR').first().select(['B4', 'B3', 'B2'])

        # Set the target size
        target_size = 100

        # Scale the image
        result = scale_image(image, target_size)
        
        # Check if the result is an ee.Image
        self.assertIsInstance(result, ee.Image)

        # Check if image is valid
        result.getInfo()

    def test_scale_collection(self):
        # Create a sample image collection
        roi  = ee.Geometry.Rectangle([-98.95, 19.34, -98.94, 19.35])

        image_collection = ee.ImageCollection('COPERNICUS/S2_SR').filterBounds(roi).filterDate('2022-01-01', '2022-01-31').select(['B4', 'B3', 'B2'])

        # Set the target size
        target_size = 100

        # Scale the image collection
        result = scale_collection(image_collection, target_size)

        # Check if the result is an ee.ImageCollection
        self.assertIsInstance(result, ee.ImageCollection)

        # Check if image collection is valid
        result.getInfo()

    def test_get_image_stats(self):
        # Create a sample image
        image = ee.ImageCollection('COPERNICUS/S2_SR').first()

        # Get image statistics
        result = get_image_stats(image)

        # Print the results

        # Check if the result is a dictionary
        self.assertIsInstance(result, ee.dictionary.Dictionary)

        # Convert to Python Dict
        result = dict(result.getInfo())

        # Check if the dictionary contains the 'Mean' key
        self.assertIn('mean', result)

        # Check if the value of 'Mean' key is a number
        self.assertIsInstance(result['mean'], dict)

    def test_get_collection_stats(self):
        # Create a sample image collection
        roi  = ee.Geometry.Rectangle([-98.95, 19.34, -98.94, 19.35])

        image_collection = ee.ImageCollection('COPERNICUS/S2_SR').filterBounds(roi).filterDate('2022-01-01', '2022-01-31')

        # Get collection statistics
        result = get_collection_stats(image_collection)

        # Check if the result is a dictionary
        self.assertIsInstance(result, dict)

    def test_coords_parsing(self):
        coords = "-98.95,19.34,-98.94,19.35"
        result = coordsToROI(coords)
        # Check the result is an ee.Geometry
        self.assertIsInstance(result, ee.Geometry)

        # Check if geometry is valid
        result.getInfo()

if __name__ == '__main__':
    unittest.main()