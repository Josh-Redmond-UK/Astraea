import ee
from .download_utils import *
from .date_time_utils import *
from .earth_engine_utils import *
import tifffile as tiff
import numpy as np
from PIL import Image  
import PIL  
import json
import tempfile
import uuid
import zipfile
import numpy as np
from PIL import Image, ImageDraw, ImageSequence

TEMP_DIR = tempfile.gettempdir()


def array_to_rbga(arr:np.ndarray) -> np.ndarray:
    ''' Function which converts an array of shape (n, m, 3) to an array of shape (n, m, 4) by adding an alpha channel 
    and masking out the nodata values.'''
    nan_mask = np.expand_dims(~np.isnan(np.sum(arr, axis=-1)) * 1, axis=-1)
    nan_mask *= 255
    nan_mask = nan_mask.astype(np.uint8)
    if arr.shape[-1] == 3:
        arr = np.concatenate((arr, nan_mask), axis=2)
    else:
        arr = np.squeeze(np.stack([arr, arr, arr, nan_mask]))


    return arr


def lognormalise(arr:np.ndarray, bottom_pct=1, top_pct=100) -> np.ndarray:
    arr = np.nan_to_num(arr)
    arr = np.log(arr)
    min = np.percentile(arr.flatten(), bottom_pct)
    max = np.percentile(arr.flatten(), top_pct)
    arr = (arr - min)/(max-min)
    return arr

def float_to_int(arr:np.ndarray) -> np.ndarray:
    return (arr * 255).astype(np.uint8)



def get_download_requests(params:dict) -> list[str]:
    print("download request params", params)
    print(type(params))
    collection = get_images_for_extent(params['roi'], params['start_date'], params['end_date'], params['cloud_cover'], params['image_type'])





    if params['agg_type'] != 'None' or params['agg_length'] != 'None':
        collection, dates = aggregate_collection(collection, params['agg_type'], params['agg_length'], params['start_date'], params['end_date'])
    
    collection = collection.map(lambda image: image.clip(coordsToROI(params['roi'])))

    img = collection.first()
    imgDescription = ee.Algorithms.Describe(img)
    height = ee.List(ee.Dictionary(ee.List(ee.Dictionary(imgDescription).get("bands")).get(0)).get("dimensions")).get(0)
    width = ee.List(ee.Dictionary(ee.List(ee.Dictionary(imgDescription).get("bands")).get(0)).get("dimensions")).get(1)
    print('height', height.getInfo())
    print('width', width.getInfo())


    collection = scale_collection(collection, 720)
    print(get_image_stats(collection.first(), geom=coordsToROI(params['roi'])).getInfo())

    urls = get_download_jobs(collection)
    return urls, dates

def process_images(image_paths:list[str]) -> list[str]:
    ''' Returns a list of paths to the processed images, converting them from tif to png format.'''
    processed_paths = []
    for i in image_paths:
        # Convert the image to png
        # Save the image to the same folder with the same name, but with the extension changed to png
        
        arr = tiff.imread(i)
        #arr = np.squeeze(np.stack([arr[:,:,j] for j in arr.shape[-1]]))
        arr = arr/np.max(arr)
        arr = float_to_int(arr)

        arr = array_to_rbga(arr)
        png_path = i[:-3] + 'png'
        Image.fromarray(arr, 'RGBA').save(png_path)
        processed_paths.append(png_path)

    return processed_paths

def create_gif(image_paths:list[str], date_list=None) -> str:
    ''' Returns the path to the created gif.'''

    if len(image_paths) > 0:
        gif_path = image_paths[0][:-3] + 'gif'
        images = [PIL.Image.open(i) for i in image_paths]
        if date_list:
            for i, img in enumerate(images):
                draw = ImageDraw.Draw(img)
                draw.text((10, 10), date_list[i], fill=(255, 255, 255, 255))



        images[0].save(gif_path, save_all=True, append_images=images[1:], duration=500, loop=0)
        return gif_path

    return ''

def generate_statistics(image_paths: list[str]) -> list[dict]:
    ''' Returns a list of dictionaries containing the statistics for each image.'''
    
    stats_list = []

    for p in image_paths:
        arr = tiff.imread(p)
        stats = [] 
        
        for band_idx in range(arr.shape[2]):
            band = arr[:, :, band_idx]
            band_stats = {
                'min': float(np.min(band)),
                'max': float(np.max(band)),
                'mean': float(np.mean(band)),
                'std': float(np.std(band))
            }
            stats.append(band_stats)
        
        image_stats = {
            'image_path': p,
            'band_stats': stats
        }
        stats_list.append(image_stats)

    return stats_list

def handle_request(params:dict) -> dict:
    ''' Returns a dictionary of the results of the specified request.'''

    # Get the download requests
    download_requests, dates = get_download_requests(params)

    # Download the images
    image_paths = download_urls(download_requests, 'downloads')
    # Process the images
    processed_image_paths = process_images(image_paths)

    # Create the gif
    gif_path = create_gif(processed_image_paths, dates)

    # Generate the statistics
    stats = generate_statistics(image_paths)
    
    all_files_list = image_paths + processed_image_paths + [gif_path]

    zip_path = create_zip(all_files_list)

    return {"ImgUrls":processed_image_paths, "GifUrl":gif_path, "Stats":stats, "ZipUrl":zip_path}

def create_zip(image_paths):
    # Generate a unique filename for the zip
    zip_filename = f"{uuid.uuid4()}.zip"
    zip_path = os.path.join(TEMP_DIR, zip_filename)
    
    with zipfile.ZipFile(zip_path, 'w') as zf:
        for img_path in image_paths:
            # Get the filename without the directory structure
            filename = os.path.basename(img_path)
            # Add file to the zip
            zf.write(img_path, filename)
    
    return zip_path



def format_response(response:dict) -> str:
    '''Returns a json string from the specified dictionary.'''
    return json.dumps(response)
