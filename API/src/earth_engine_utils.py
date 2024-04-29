import ee
from .date_time_utils import *
from datetime import datetime


def get_BAIS2(image):
    ''' Returns an image with a new spectral band representing the BAIS2 index.
    
    Parameters:
    image (ee.Image): The image to calculate the index for.

    Returns:
    ee.Image: The image with the new spectral band with a name matching the index type (e.g. 'BAIS2')
    '''
    # Calculates the Burnt Area Index adjusted for Sentinel-2 using the method outlined in: https://www.mdpi.com/2504-3900/2/7/364

    B4 = image.select(['B4'])
    B6 = image.select(['B6'])
    B7 = image.select(['B7'])
    B8A = image.select(['B8A'])
    B12 = image.select(['B12'])

    return image.expression('1-sqrt(B6*B7*B8A/B4)*((B12-B8A)/sqrt(B12+B8A) + 1)', {"B4": B4, "B6": B6, "B7": B7,
    "B8A": B8A, "B12":B12}).rename('BAIS2')

def get_NBR(image):
    ''' Returns an image with a new spectral band representing the NBR index.
    
    Parameters:
    image (ee.Image): The image to calculate the index for.

    Returns:
    ee.Image: The image with the new spectral band with a name matching the index type (e.g. 'NBR')
    '''

    return image.normalizedDifference(['B8', 'B12']).rename('NBR')

def get_NDVI(image):
    ''' Returns an image with a new spectral band representing the NDVI index.
    
    Parameters:
    image (ee.Image): The image to calculate the index for.

    Returns:
    ee.Image: The image with the new spectral band with a name matching the index type (e.g. 'NDVI')
    '''

    return image.normalizedDifference(['B8', 'B4']).rename('NDVI')



def get_spectral_index(image_collection, index_type:str):
    ''' Returns an image collection with a new spectral band representing the specified index.
    
    Parameters:
    image_collection (ee.ImageCollection): The image collection to calculate the index for.
    index_type (str): The index to calculate. Currently supports NDVI, NBR, and BAIS2

    Returns:
    ee.ImageCollection: The image collection with the new spectral band with a name matching the index type (e.g. 'NDVI')
    '''

    
    match index_type:
        case 'NDVI':
            return image_collection.map(get_NDVI)
        case 'NBR':
            return image_collection.map(get_NBR)
        case 'BAIS2':
            return image_collection.map(get_BAIS2)
        case 'Colour':
            return image_collection.select(['B4', 'B3', 'B2'])
        case _:
            raise ValueError(f'Index type {index_type} is not supported. Please use NDVI, NBR, or BAIS2.')
        
def coordsToROI(coords):
    '''Converts a string of coordinates to an ee.Geometry object.'''
    stringList = coords.split(',')
    coordsNum = [float(x) for x in stringList]
    it = iter(coordsNum)
    coords = [*zip(it, it)]
    if len(coords) >= 3:
        roi = ee.Geometry.Polygon(coords)
    else:
        roi = ee.Geometry.Rectangle(coordsNum)

    return roi



def get_images_for_extent(roi:ee.geometry, start_date:str, end_date:str, cloud_cover:float, spectral_index:str):
    ''' Returns an image collection of Sentinel-2 imagery with a new spectral band representing the specified index.
    
    Parameters:
    roi (ee.geometry): The region of interest to get images for.
    start_date (str): The start date for the image collection.
    end_date (str): The end date for the image collection.
    cloud_cover (float): The maximum cloud cover for the image collection.
    spectral_index (str): The index to calculate. Currently supports NDVI, NBR, and BAIS2

    Returns:
    ee.ImageCollection: The image collection with the new spectral band with a name matching the index type (e.g. 'NDVI')
    '''
    if type(roi) == str:
        roi = coordsToROI(roi)

    # Filters the image collection by the specified parameters
    image_collection = ee.ImageCollection('COPERNICUS/S2_SR').filterBounds(roi).filterDate(start_date, end_date).filter(ee.Filter.lte('CLOUDY_PIXEL_PERCENTAGE', cloud_cover))

    # Calculates the specified spectral index for the image collection
    image_collection = get_spectral_index(image_collection, spectral_index)

    
    return image_collection


def aggregate_collection(image_collection:ee.imagecollection, aggregation_type:str, aggregation_length:str, start_date:str, end_date:str):
    ''' Returns an image collection temporally aggregated according to the specified aggregation type and length. For example, if the aggregation
    type is mean and the aggregation length is monthly, then the image collection will be aggregated to monthly means for the specified date range. 
    Images in the collection which fall outside of the specified date range will be removed.
    
    Parameters:
    image_collection (ee.ImageCollection): The image collection to aggregate.
    aggregation_type (str): The aggregation type. Currently supports mean, median, maximum, and max_change.
    aggregation_length (str): The aggregation length. Currently supports monthly and yearly.
    start_date (str): The start date for the aggregation.
    end_date (str): The end date for the aggregation.
    
    
    Returns:
    ee.ImageCollection: The aggregated image collection.
    '''
    #print(f'Aggregating collection with {aggregation_type} {aggregation_length} from {start_date} to {end_date}')

    match aggregation_type:
        case "mean":
            def agg_func(image_collection):
                return image_collection.mean()
        case "median":
            def agg_func(image_collection):
                return image_collection.median()
        case "maximum":
            def agg_func(image_collection):
                return image_collection.max()
        case "max_change":
            pass
        case _:
            raise ValueError(f'Aggregation type {aggregation_type} is not supported. Please use mean, median, maximum, or max_change.')
        
    match aggregation_length:
        case "monthly":
            image_collection = ee.ImageCollection([agg_func(image_collection.filterDate(month[0], month[1])).setDefaultProjection("EPSG:3857", scale=10) for month in get_months(start_date, end_date)])
            #image_collection = ee.List(get_months(start_date, end_date)).map(lambda month: agg_func(image_collection.filterDate(month[0], month[1])))
        case "annual":
            #image_collection = ee.List(get_years(start_date, end_date)).map(lambda month: agg_func(image_collection.filterDate(month[0], month[1])))
            image_collection = ee.ImageCollection([agg_func(image_collection.filterDate(year[0], year[1])).setDefaultProjection("EPSG:3857", scale=10) for year in get_years(start_date, end_date)])
        case "none":
            #print("No aggregation returning median for whole collection yolo") 
            image_collection = ee.ImageCollection([image_collection.median()])
        case _:
            raise ValueError(f'Aggregation length {aggregation_length} is not supported. Please use Monthly, Annual, or None.')


    
    return image_collection


def numberOfPixels(img:ee.image):
    """
    Calculates the number of pixels in an image.

    Parameters:
        img (ee.Image): The input image.

    Returns:
        tuple: A tuple containing the width and height of the image in ee.Number format.
    """
    imgDescription = ee.Algorithms.Describe(img)
    height = ee.List(ee.Dictionary(ee.List(ee.Dictionary(imgDescription).get("bands")).get(0)).get("dimensions")).get(0)
    width = ee.List(ee.Dictionary(ee.List(ee.Dictionary(imgDescription).get("bands")).get(0)).get("dimensions")).get(1)


    return ee.Number(width), ee.Number(height)


def convert_projection_resolution(image:ee.image, target_size:int):
    ''' Uses the image's project information to calculate a new projection with a resolution that is as close as possible to the target size.
    
    Parameters:
        image (ee.Image): The image to calculate the new projection for.
        target_size (int): The maximum size of the largest dimension of the image in pixels.
    '''
    proj = image.projection()
    image_scale = proj.nominalScale()
    w, h = numberOfPixels(image)
    maxdim = w.max(h)

    new_scale = maxdim.divide(target_size).multiply(image_scale)

    return proj.atScale(new_scale)

def scale_image(image, target_size):
    ''' Scales an image to the specified target size using convert_projection_resolution'''
    return image.reproject(convert_projection_resolution(image, target_size))

def scale_collection(image_collection, target_size):
    ''' Scales an image collection to the specified target size using convert_projection_resolution'''
    return image_collection.map(lambda image: scale_image(image, target_size))

def collection_stats(image_collection:ee.imagecollection) -> dict:
    ''' Returns a dictionary containing the image-level statistics of each image in an image collectiion.'''

    
def get_image_stats(image:ee.image, geom=None) -> dict:
    ''' Returns a dictionary containing the per-band image-level statistics of an image.'''
    if geom is None:
        geom = image.geometry()
    mean = image.reduceRegion(ee.Reducer.mean(), geom, 10, bestEffort=True)
    max = image.reduceRegion(ee.Reducer.max(), geom, 10, bestEffort=True)
    min = image.reduceRegion(ee.Reducer.min(), geom, 10, bestEffort=True)

    stats_dict = ee.Dictionary({'mean': mean, 'max': max, 'min': min})

    return stats_dict

def get_collection_stats(collection:ee.imagecollection) -> dict:
    dates = collection.aggregate_array('system:time_start').getInfo()
    dates = [datetime.fromtimestamp(i/1000).strftime('%Y-%m-%d') for i in dates]
    num_images = collection.size()
    images = collection.toList(num_images)

    stats = [get_image_stats(ee.Image(images.get(i))).getInfo() for i in range(num_images.getInfo())]

    return dict(zip(dates, stats))


