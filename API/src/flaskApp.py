from utils import *
from flask import Flask
from flask import request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

ee.Initialize()

global currentData
global zipPayload
global activeCollection

@app.route('/')
def helloWorld():
    return "hello!"

@app.route('/api/mapping', methods=['GET'])
def generatePaths():
    clean_up_wd()
    zipPayload = None
    imageType = request.args['imagery-type']
    print("image type", imageType)
    endDate = request.args['end-date']
    startDate = request.args['start-date']

    aggregationType = request.args['aggregation-type']
    print("aggtype", aggregationType)
    aggregationLength = request.args['aggregation-length']
    print("agglength", aggregationLength)
    coords = request.args["coords"]

    

    name, dates, paths, col = webGeneratePaths(coords, (ee.Date(str(startDate)), ee.Date(str(endDate))), imageType, aggregationLength, aggregationType, 100)
    gifPath = create_gif(paths, name)
    currentData = (name, dates, paths, col)
    roi = coordsToROI(coords)
    boundsGeom = roi.getInfo()['coordinates']

    coordFrame = pd.DataFrame(boundsGeom[0], columns=["Lat", 'Lon'])
    s = min(coordFrame['Lat'])
    n = max(coordFrame['Lat'])
    w = min(coordFrame['Lon'])
    e = max(coordFrame['Lon'])

    sw = (s,w)
    ne = (n,e)

    response = jsonify(name=name, dates=dates, gifUrl=gifPath, sw=sw, ne=ne)

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@app.route('/api/mapping/download', methods=['GET'])
def serveZip():
    if zipPayload!= None:
        foo
    else:
        name, dates, paths, col = currentData

