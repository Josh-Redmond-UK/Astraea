from flask import Flask
from flask import request, jsonify
from src import utils
import ee
from ipyleaflet import Map, basemaps, basemap_to_tiles

ee.Initialize()



app = Flask(__name__)



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

   # imageType = request.args['ImageType']
   # startDate = request.args['startDate']
   # endDate = request.args['endDate']
   # aggregationType = request.args['aggType']
   # aggregationLength = request.args['aggLen']
   # geomJson = request.args["geom"]
    
   # roi = ee.Geometry.Polygon(geomJson)
    m = Map(
    basemap=basemap_to_tiles(basemaps.NASAGIBS.ModisTerraTrueColorCR, "2017-04-08"),
    center=(52.204793, 360.121558),
    zoom=4)

    

    return str(id * 100)
