import ee
import ipywidgets as widgets
import pandas as pd
from PIL import Image
import imageio
from geopy.geocoders import Nominatim
import os
import numpy as np
import matplotlib.pyplot as plt
import requests
import shutil
import tifffile
import base64
from zipfile import ZipFile
import glob
from tifffile.tifffile import TiffSequence
from IPython.core.display import display
import calendar
import os.path


def coordsToROI(coords):
    stringList = coords.split(',')
    coordsNum = [float(x) for x in stringList]
    it = iter(coordsNum)
    coords = [*zip(it, it)]
    roi = ee.Geometry.Polygon(coords)
    return roi

def clipImgCol(imgCol, roi):
    return imgCol.map(lambda x: x.clip(roi))

def webGetCollection(roi, dateRange, maxCloud=100):
    startDate, endDate = dateRange
    areaOfInterest = roi

    s2Collection = ee.ImageCollection("COPERNICUS/S2").filterDate(startDate, endDate).filterMetadata(
    'CLOUDY_PIXEL_PERCENTAGE', 'less_than',maxCloud).filterBounds(areaOfInterest)
    s2Clipped = clipImgCol(s2Collection, roi)

    cLon, cLat = areaOfInterest.centroid(200).getInfo()['coordinates']
    areaName = reverse_geocode_area(cLon, cLat)
    return s2Clipped, areaName

def webAggregateCollection(collection, imageType, aggLength, aggType):

    dates = ymdList(collection)

    bands_order_dict = {"Burnt Area Index" : ['constant'],
                        "Grey Green Blue Index":["red", "green", "blue"],
                        "True Colour" : ['B4',  'B3', 'B2'],
                        "NBR" : ['constant',"B3","B2"],
                        "NDVI" : ["B4", 'constant', "B2"]}


    aggregation_options_dict = {"Monthly": aggregate_monthly(collection, dates, aggType),
                       "Annual": aggregate_anually(collection, dates, aggType),
                       "None": (collection, dates)}

    GeneratedCollection, dates = aggregation_options_dict[aggLength]



    image_col_dict = {"Burnt Area Index": GeneratedCollection.map(get_BAIS2),
                        "Grey Green Blue Index": GeneratedCollection.map(get_Green_Grey_Blue_Index),
                      "True Colour": GeneratedCollection.map(lambda x: x.divide(10000)),
                      "NBR": GeneratedCollection.map(add_NBR).map(reproject_to_calc_band),
                      "NDVI": GeneratedCollection.map(add_NDVI).map(reproject_to_calc_band)}
    
    GeneratedCollection = image_col_dict[imageType]
    selectedBands = bands_order_dict[imageType]

    return GeneratedCollection, selectedBands, dates

def downloadImages(GeneratedCollection, selectedBands):
    paths = get_imagecollection_download(GeneratedCollection.map(lambda x: x.select(selectedBands)))
    return paths


def webGeneratePaths(coordsList, dateRange, imageType, aggLength, aggType, maxCloud):
    roi = coordsToROI(coordsList)
    col, name = webGetCollection(roi, dateRange, maxCloud)
    col, bands, dates = webAggregateCollection(col, imageType, aggLength, aggType)
    paths = downloadImages(col, bands)
    return name, dates, paths, col

def clean_up_wd():
    tiffs = glob.glob("*.tif")
    gifs = glob.glob("*.gif")
    piffs = glob.glob("*.pdf")
    ziffs = glob.glob("*.zip")

    to_delete = tiffs + gifs + piffs + ziffs
    for file in to_delete:
        os.remove(file)



def reverse_geocode_area(lon, lat):
    locator = Nominatim(user_agent="jr725@exeter.ac.uk")
    coordinates = f"{lat}, {lon}"
    location = locator.reverse(coordinates)
    location_return = location.raw
    
    return location_return['display_name']

def get_imgcol_roi(imgcol, roi):

    clipped_col = imgcol.filterBounds(roi).map(lambda img: img.clip(roi))

    return clipped_col

def get_s2_metadata(imgcol):

    dates = imgcol.reduceColumns(ee.Reducer.toList(), ['system:time_start']).getInfo()
    return dates

def get_BAIS2(image):
    # Calculates the Burnt Area Indes adjusted for Sentinel-2 using the method outlined in: https://www.mdpi.com/2504-3900/2/7/364
   
    B4 = image.select(['B4'])#.divide(10000)
    B6 = image.select(['B6'])#.divide(10000)
    B7 = image.select(['B7'])#.divide(10000)
    B8A = image.select(['B8A'])#.divide(10000)
    B12 = image.select(['B12'])#.divide(10000)

    return image.expression('1-sqrt(B6*B7*B8A/B4)*((B12-B8A)/sqrt(B12+B8A) + 1)', {"B4": B4, "B6": B6, "B7": B7,
    "B8A": B8A, "B12":B12})

## Repetition of Add_xx functions so each can be called as an argument of map using the EE API which doesn't support mapping functions with arguments
def add_BAIS2(image):
    return image.cat(get_BAIS2(image), image.select("B3").divide(10000), image.select("B2").divide(10000))


def get_NBR(image):
    nbr_3 = image.normalizedDifference(['B8', 'B12']).rename('constant')
    return nbr_3

def add_NBR(image):
    return image.addBands([get_NBR(image)]).select(["constant", "B3", "B2"])
    
def get_NDWI(image):
    NDWI = image.normalizedDifference(['B3', 'B8']).rename("NDWI")
    return NDWI

def get_NDBI(image):
    NDBI = image.normalizedDifference(['B11', 'B8']).rename("NDBI")
    return NDBI

def get_Green_Grey_Blue_Index(image):
    red = get_NDBI(image).rename("red")
    green = get_NDVI(image).rename("green")
    blue = get_NDWI(image).rename("blue")

    return red.addBands([green, blue])




def get_NDVI(image):
    NDVI = image.normalizedDifference(['B8', 'B4']).rename("constant")
    return NDVI


def add_NDVI(image):
    return image.addBands([get_NDVI(image)]).select(["B4","constant", "B2"])
    



def create_dummy_input_frame():

    frame = pd.DataFrame(columns=["Lat", "Lon"])
    return frame


def reproject_to_calc_band(image):
    calc_proj = image.select("constant").projection()
    reproj = image.reproject(calc_proj)
    return reproj


def add_new_latlon_row(frame, lat, lon):
    frame.loc[len(frame)] = [lat, lon]

def numberOfPixels(img):
  
    imgDescription = ee.Algorithms.Describe( img )
    height = ee.List( ee.Dictionary( ee.List(  ee.Dictionary(imgDescription ).get("bands") ).get(0) ).get("dimensions") ).get(0)
    width = ee.List( ee.Dictionary( ee.List(  ee.Dictionary(imgDescription ).get("bands") ).get(0) ).get("dimensions") ).get(1)

    return  ee.Number( width ), ee.Number( height )

def ymdList(imgcol):
    def iter_func(image, newlist):
        date = image.date().format("YYYY-MM-dd")
        newlist = ee.List(newlist)
        return ee.List(newlist.add(date).sort())
    ymd = imgcol.iterate(iter_func, ee.List([]))
    return ee.List(ymd).getInfo()


def plot_raster_map():
    pass

class Area_Analysis(ee.ImageCollection):
    def __init__(self, image_collection, gif_path, title, bands, bounds, image_mode, dates, framesPath):
        super().__init__(image_collection)
        
        self.dates = dates
        self.gif_path = gif_path
        self.title = title
        self.bands = bands
        self.bounds = bounds
        self.framesPath = framesPath
        self.image_mode = image_mode

    
    def display(self):

        im = Image.open(self.gif_path)

        frames = 0
        try:
            while 1:
                im.seek(im.tell()+1)
                frames +=1

        except EOFError:
            pass 
        
        image_display = widgets.Output()
        text_display = widgets.Output()
                
        image_display = widgets.Output()
        play_button = widgets.Play(value=1, min=1, max=frames+1, step=1, interval=1000)
        slider = widgets.IntSlider(value=1, min=1, max=frames+1)
        widgets.jslink((play_button, 'value'), (slider, 'value'))
        gifheight = im.size[1]
        image_display.layout.height = f'{gifheight}px'
        im.seek(1)
        with image_display:
            image_display.clear_output()
            display(im)


        def update_image_frame(b):
                im.seek(slider.value)
                with image_display:
                    image_display.clear_output()
                    display(im)
        

        slider.observe(update_image_frame)

    
        gif_controls = widgets.HBox([play_button, slider])
        roi_analysis_widget = widgets.VBox([image_display, gif_controls])
        return roi_analysis_widget

    def export(self):
        # Generates set of PDF maps with metadata for an observation and displays images for each frame in sequence
        num_images = self.size().getInfo()

        ee_images_list = self.toList(num_images)

        bounds = self.bounds
        dates = self.dates
        title = self.title
        image_mode = self.image_mode

    
        lon, lat = bounds.centroid(200).getInfo()['coordinates']
        area_string = reverse_geocode_area(lon=lon, lat=lat)
    
        # Get bounds from earth engine
        bounds_frame = pd.DataFrame(np.array(bounds.bounds().getInfo()['coordinates'][0]), columns=["Lon", "Lat"])
        min_lon = bounds_frame['Lon'].min()
        max_lon = bounds_frame['Lon'].max()
        min_lat = bounds_frame['Lat'].min()
        max_lat = bounds_frame['Lat'].max()


        images_list = []

        for i in range(num_images):
            images_list.append(ee.Image(ee_images_list.get(i)))

       # pickle_path = title+".pickle"

       # with open(pickle_path, "wb") as handle:
       #     pickle.dump(self, handle, protocol=pickle.HIGHEST_PROTOCOL)
        # Uses an fstring to create and serve an html download button containing the analysed data using lazy execution (to not delay the user)

        #BUTTONS
        html_buttons = f'''<html>
        <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body>
        <a download="{title+'.zip'}" href="data:text/csv;base64,{generate_and_serve_zip_payload(images_list, (min_lon, max_lon, min_lat, max_lat), self.bands, title, dates, image_mode, area_string, additional_paths=[self.gif_path], framesPath = self.framesPath)}" download>
        <button class="p-Widget jupyter-widgets jupyter-button widget-button mod-warning">Download File</button>
        </a>
        </body>
        </html>
        '''

        html_button = html_buttons#.format(payload=payload,filename=filename)
        return html_button


def generate_and_serve_zip_payload(images_list, bounds_tuple, bands, title, dates, image_mode, area_string, framesPath, additional_paths=None):
    paths = generate_maps(images_list, bounds_tuple, bands, title, dates, image_mode, area_string, framesPath)
    paths += additional_paths
    zip_path = generate_zip(paths, title)
    with open(zip_path, "rb") as zip_to_serve:
        payload = base64.b64encode(zip_to_serve.read()).decode()

    return payload


def convert_image_resolution(image, gif_size=1280):
    # converts image from one resolution to another according to a target size - so it can be sent to a gif easily
        proj = image.projection()
        image_scale = ee.Number(10)#proj.nominalScale()
        w, h = numberOfPixels(image)
        maxdim = w.max(h)

        new_scale = maxdim.divide(gif_size).multiply(image_scale)

        return proj.atScale(new_scale)

def downscale_image(image, max_image_size = 1280):
    #max_image_size = 1920
    new_projection = convert_image_resolution(image, max_image_size)

    #downscaled = image.reduceResolution(ee.Reducer.mean(),bestEffort=True).reproject(new_projection)
    downscaled = image.reproject(new_projection)
    #print("downscaling completed")
    return downscaled

#def reproject_imgcol()


def aggregate_monthly(img_col, datelist, mode="Mean"):
    #datelist = ymdList(img_col)
    dates_conv = pd.to_datetime(datelist, dayfirst=False)
    months = []
    for d in dates_conv:
        months.append([d.year, d.month])


    unique_months = []
    for m in months:
        if m not in unique_months:
            unique_months.append(m)


    months_starts_ends = []

    for m in unique_months:
        
        
        date_range = calendar.monthrange(m[0], m[1])
        
        month = m[1]
        if len(str(month)) == 1:
            month = "0"+str(month)
        
        months_starts_ends.append((f"{m[0]}-{month}-01", f"{m[0]}-{month}-{date_range[1]}"))

    monthly_composites = []
    starts = []
    for m in months_starts_ends:
        
        try:
            monthly_dict = {"Mean":img_col.filterDate(m[0], m[1]).mean().setDefaultProjection("EPSG:3857", scale=10),
                        "Median":img_col.filterDate(m[0], m[1]).median().setDefaultProjection("EPSG:3857", scale=10), 
                        "Max":img_col.filterDate(m[0], m[1]).qualityMosaic("constant").setDefaultProjection("EPSG:3857", scale=10)}
        
        except:
            monthly_dict = {"Mean":img_col.filterDate(m[0], m[1]).mean().setDefaultProjection("EPSG:3857", scale=10),
                "Median":img_col.filterDate(m[0], m[1]).median().setDefaultProjection("EPSG:3857", scale=10), 
                "Max":img_col.filterDate(m[0], m[1]).max().setDefaultProjection("EPSG:3857", scale=10)}
        
        
        monthly_collection = monthly_dict[mode]#img_col.filterDate(m[0], m[1]).mean().setDefaultProjection("EPSG:3857", scale=10)
        monthly_composites.append(monthly_collection)
        starts.append(m[0])

    return (ee.ImageCollection(monthly_composites), starts)
                        


def aggregate_anually(img_col, datelist, mode="Mean"):
    #datelist = ymdList(img_col)
    dates_conv = pd.to_datetime(datelist, dayfirst=False)
    years = []
    for d in dates_conv:
        years.append(d.year)


    unique_years = []
    for y in years:
        if y not in unique_years:
            unique_years.append(y)


    years_starts_ends = []
    for y in unique_years:


        date_range = calendar.monthrange(1, 12)

        #month = m[1]
        #if len(str(month)) == 1:
        #    month = "0"+str(month)

        years_starts_ends.append((f"{y}-01-01", f"{y}-12-31"))

    annual_composites = []
    starts = []
    for y in years_starts_ends:
        
        try:
            annual_dict = {"Mean":img_col.filterDate(y[0], y[1]).mean().setDefaultProjection("EPSG:3857", scale=10),
                            "Median":img_col.filterDate(y[0],y[1]).median().setDefaultProjection("EPSG:3857", scale=10), 
                            "Max":img_col.filterDate(y[0], y[1]).qualityMosaic("constant").setDefaultProjection("EPSG:3857", scale=10)}
        except:
            annual_dict = {"Mean":img_col.filterDate(y[0], y[1]).mean().setDefaultProjection("EPSG:3857", scale=10),
                "Median":img_col.filterDate(y[0],y[1]).median().setDefaultProjection("EPSG:3857", scale=10), 
                "Max":img_col.filterDate(y[0], y[1]).max().setDefaultProjection("EPSG:3857", scale=10)}


        annual_collection = annual_dict[mode]#img_col.filterDate(m[0], m[1]).mean().setDefaultProjection("EPSG:3857", scale=10)
        annual_composites.append(annual_collection)
        starts.append(y[0])

    return (ee.ImageCollection(annual_composites), starts)

                        
                        
                        
    
def get_imagecollection_download(img_col):
    num_images = img_col.size().getInfo()

    images_list = img_col.toList(num_images)

    downloaded_images = []
    for idx, img in enumerate(images_list):
    #reproject("EPSG:3857")
        test_url = img.getDownloadURL(params={
            "format" : "GEO_TIFF"})

        test_r = requests.get(test_url, stream=True)
        print(test_url)
        #print(test_url)
        #print(test_r)v os.path.dirname(__file__) + f'/../../../'
        path = os.path.dirname(__file__) + '/../../../'+'frame'+str(idx)+'.tif'
        assert test_r.status_code == 200
        with open(path, 'wb') as f:
            test_r.raw.decode_content = True
            shutil.copyfileobj(test_r.raw, f)
        downloaded_images.append(path)
    return downloaded_images


def generate_maps(images_list, bounds_tuple, bands, title, dates, image_mode, area_string, framesPath):
    min_lon, max_lon, min_lat, max_lat = bounds_tuple
    #print(framesPath)
    downloaded_images = []
    arrays = []
    for f in framesPath:
        array = tifffile.imread(f)
        #print(array.shape)
        for band in range(array.shape[2]):
            array[:,:,band] = ((array[:,:,band] - array[:,:,band].min()) * (1/(array[:,:,band].max() - array[:,:,band].min()) * 255)).astype('uint8')
        arrays.append(array.astype('uint8'))
        #####



    nrows = len(arrays)
    fig, axes = plt.subplots(figsize=(16.5, 11.75*nrows), nrows=nrows)

    axes = axes.flatten()
    for idx, ar in enumerate(arrays):

        img_extent = (min_lon, max_lon, min_lat, max_lat)
        x_size = abs(min_lon-max_lon)
        y_size = abs(min_lat-max_lat)
        x_buffer = x_size * 0.025
        y_buffer = y_size * 0.025
        title = f"{area_string}, {dates[idx]}, {image_mode}"
        test_extent = (min_lon-x_buffer, max_lon+x_buffer, min_lat-x_buffer, max_lat+x_buffer)
        #axes[idx] = plt.axes(projection=ccrs.PlateCarree())
        axes[idx]#.stock_img()
        axes[idx].imshow(ar, extent=img_extent)
        #axes[idx].set_extent(test_extent)
        #lines = axes[idx].gridlines(draw_labels=True, alpha=0.5, ls="--")
        #lines.xlabels_top = False
        #lines.ylabels_right = False
        axes[idx].title.set_text(title)
    
    nrows = len(arrays)
    fig, axes = plt.subplots(figsize=(16.5, 11.75*nrows), nrows=nrows)

    axes = axes.flatten()
    for idx, ar in enumerate(arrays):

        img_extent = (min_lon, max_lon, min_lat, max_lat)
        x_size = abs(min_lon-max_lon)
        y_size = abs(min_lat-max_lat)
        x_buffer = x_size * 0.025
        y_buffer = y_size * 0.025
        title = f"{area_string}, {dates[idx]}, {image_mode}"
        test_extent = (min_lon-x_buffer, max_lon+x_buffer, min_lat-y_buffer, max_lat+y_buffer)
        #axes[idx] = plt.axes(projection=ccrs.PlateCarree())
        axes[idx]#.stock_img()
        axes[idx].imshow(ar, extent=img_extent)
        #axes[idx].set_extent(test_extent)
        #lines = axes[idx].gridlines(draw_labels=True, alpha=0.5, ls="--")
        #lines.xlabels_top = False
        #lines.ylabels_right = False
        axes[idx].title.set_text(title)
    #path = os.path.dirname(__file__) + f'/../../../'
    pdf_path =  os.path.dirname(__file__) + f'/../../../'+title+".pdf"
    fig.savefig(pdf_path, orientation="landscape")
    plt.close()
    return [pdf_path, *downloaded_images]


    
def generate_zip(paths, title):
    zip_path = title+'.zip'

    with ZipFile(zip_path, 'w') as zipObj2:
        # Adds the pdf map, geotiffs and video to a zip file
        for p in paths:
            zipObj2.write(p)

    return zip_path

def get_imagecollection_download(img_col):
    num_images = img_col.size().getInfo()

    ee_images_list = img_col.toList(num_images)
    images_list = []
    
    for i in range(num_images):
        images_list.append(ee.Image(ee_images_list.get(i)))

    downloaded_images = []
    progressBar = widgets.IntProgress(value = 0, min = 0, max = len(images_list))
    for idx, img in enumerate(images_list):
    #reproject("EPSG:3857")
        scale = convert_image_resolution(img, 1440).nominalScale()
    
    
        test_url = img.getDownloadURL(params={
            "format" : "GEO_TIFF",
            "scale": scale})
        #print(test_url)
        test_r = requests.get(test_url, stream=True)
        #print(test_url)
        #print(test_r)
        path = os.path.dirname(__file__) + f'/../../../{idx}.tif'

        #path = './frame'+str(idx)+'.tif'
        print( test_r.status_code)
        assert test_r.status_code == 200
        with open(path, 'wb') as f:
            test_r.raw.decode_content = True
            shutil.copyfileobj(test_r.raw, f)
        downloaded_images.append(path)
        progressBar.value += 1 
    del(progressBar)
    return downloaded_images

def create_gif(frame_paths, title, fps=1):
    images = [imageio.imread(path) for path in frame_paths]
    images = [np.clip(i/np.max(i)*255, 0, 255).astype(np.uint8) for i in images]
    gif_title = os.path.dirname(__file__) + f'/../../../{title}.gif'
    imageio.mimsave(gif_title, images, fps=1)
    
def download_gif(img_col, title="Animation", fps=1):
    frame_paths = get_imagecollection_download(img_col)
    create_gif(frame_paths, title, fps)
    return frame_paths