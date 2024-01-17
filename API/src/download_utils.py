import ee
import shutil
import os
import requests
from retry import retry

def download_image(image_url: str, path: str) -> str:
    ''' Downloads an image from Earth Engine to the specified path.
    
    Parameters:
    image_url (str): The URL of the image to download.
    path (str): The path to save the downloaded image.
    
    Returns:
    str: The path of the downloaded image.
    '''

    r = requests.get(image_url, stream=True)

    assert r.status_code == 200
    with open(path, 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)

    return path

def get_url(image_list: ee.List, idx: int) -> str:
    ''' Returns the download URL of an image from the Earth Engine image list.
    
    Parameters:
    image_list (ee.List): The Earth Engine image list.
    idx (int): The index of the image in the list.
    path (str): The path to save the downloaded image.
    
    Returns:
    str: The download URL of the image.
    '''
    image = ee.Image(image_list.get(idx))
    print("nominal scale", image.projection().nominalScale().getInfo())
    image_url = image.getDownloadURL(params={
        "format" : "GEO_TIFF",
        "scale": image.projection().nominalScale().getInfo(),
        "region":image.geometry()})
    return image_url

def download_urls(url_list: list[str], folder_path: str, file_type='tif') -> list[str]:
    ''' Downloads a list of URLs to the specified folder path.
    
    Parameters:
    url_list (List[str]): The list of URLs to download.
    folder_path (str): The folder path to download the URLs to.
    
    Returns:
    List[str]: A list of paths to the downloaded images.
    '''
    tif_paths = []
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    for idx, url in enumerate(url_list):
        path = os.path.join(folder_path, f'image_{idx}.{file_type}')
        tif_paths.append(download_image(url, path))

    return tif_paths

def get_download_jobs(imagecollection: ee.ImageCollection) -> list[str]:
    ''' Returns a list of download jobs for the specified image collection. 
    Each job can be individually passed to download_image() to download the image to the specified path.
    
    Parameters:
    imagecollection (ee.ImageCollection): The image collection to get download jobs for.
    
    Returns:
    List[str]: A list of download jobs for the specified image collection.
    '''
    
    # Get the list of images in the collection
    images = imagecollection.toList(imagecollection.size())
    num_images = images.size().getInfo()

    # Initialize the list of download jobs
    job_idxs = list(range(num_images))
    url_list =  [get_url(images, idx) for idx in job_idxs]

    return url_list
