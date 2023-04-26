from flask import Flask
from flask import request, jsonify
from src import utils
import geemap as ge
import pandas as pd
import os
import ee
from ipyleaflet import Map, basemaps, basemap_to_tiles

ee.Initialize()



app = Flask(__name__)

def reverse_geocode_area(lon, lat):
    locator = Nominatim(user_agent="jr725@exeter.ac.uk")
    coordinates = f"{lat}, {lon}"
    location = locator.reverse(coordinates)
    location_return = location.raw
    
    return location_return


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


# A route to return all of the available entries in our catalog.
@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(books)

@app.route('/api/mapping', methods=['GET'])
def GetImagery():

    imageType = request.args['ImageType']
    startDate = request.args['startDate']
    endDate = request.args['endDate']
    aggregationType = request.args['aggType']
    aggregationLength = request.args['aggLen']
    geomJson = request.args["geom"]
    
    roi = ee.Geometry.Polygon(geomJson)
    # Get ROI and bounds of input geometry
    bounds_frame = pd.DataFrame(np.array(roi.bounds().getInfo()['coordinates'][0]), columns=["Lon", "Lat"])
    min_lon = bounds_frame['Lon'].min()
    max_lon = bounds_frame['Lon'].max()
    min_lat = bounds_frame['Lat'].min()
    max_lat = bounds_frame['Lat'].max()
    video_bounds = ((min_lat, min_lon), (max_lat, max_lon))

    start = startDate.strftime("%Y-%m-%d")
    end = endDate.strftime("%Y-%m-%d")

    s2Filtered = ee.ImageCollection("COPERNICUS/S2").filterDate(start, end).filterBounds(roi)#.filterMetadata(
        #'CLOUDY_PIXEL_PERCENTAGE', 'less_than',cloud_cover_qual.value)
    s2Filtered = utils.get_imgcol_roi(s2Filtered, roi)

    dates = utils.ymdList(s2Filtered)
    #s2Clipped = s2Filtered.map(lambda x: x.clip(roi))

    aggregation_options_dict = {"Monthly": utils.aggregate_monthly(s2Filtered, dates, aggregationType),
                    "Annual": utils.aggregate_anually(s2Filtered, dates, aggregationType),
                    "None": (s2Filtered, dates)}


    GeneratedCollection, dates = aggregation_options_dict[aggregationLength]

    bands_order_dict = {"Burnt Area Index" : ['constant'],
                        "Grey Green Blue Index":["red", "green", "blue"],
                        "True Colour" : ['B4',  'B3', 'B2'],
                        "NBR" : ['constant',"B3","B2"],
                        "NDVI" : ["B4", 'constant', "B2"]}

    image_col_dict = {"Burnt Area Index": GeneratedCollection.map(utils.get_BAIS2),
                            "Grey Green Blue Index": GeneratedCollection.map(utils.get_Green_Grey_Blue_Index),
                        "True Colour": GeneratedCollection.map(lambda x: x.divide(10000)),
                        "NBR": GeneratedCollection.map(utils.add_NBR).map(utils.reproject_to_calc_band),
                        "NDVI": GeneratedCollection.map(utils.add_NDVI).map(utils.reproject_to_calc_band)}


    GeneratedCollection = image_col_dict[imageType]
    selected_bands = bands_order_dict[imageType]

    lon, lat = roi.centroid(200).getInfo()['coordinates']
    area_string = utils.reverse_geocode_area(lon=lon, lat=lat)
    title = f"{area_string}, {start}-{end}, {imageType}"
    saved_gif = title+".gif"

    saved_gif = os.path.join(os.path.dirname(os.getcwd()), saved_gif)


    framePaths = utils.download_gif(GeneratedCollection.select(selected_bands).map(lambda x: x.clip(roi)), title)
    ge.add_text_to_gif(saved_gif, saved_gif, xy=('0%', '0%'), text_sequence=dates, font_color='white', duration=1000)
    
    # Filter by date to select S2 imagery
    # Create slideshow 
    # Create files - zip, pdf, gifs and tifs
    # Return json with
    # Link to gif to show
    # Link to Tifs for carousel? OPTIONAL FOR NOW
    # Link to zip for download (download link)