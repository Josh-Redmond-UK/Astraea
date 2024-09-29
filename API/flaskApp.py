from src.utils import *
from src.api_utils import handle_request
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
    print(request.args)
    data = request.args['params']
    print(data)
    clean_up_wd()
    print("handling request for data", data)
    handle_request(data)

    zipPayload = None
    imageType = data['image_type']
    print("image type", imageType)
    endDate = data['end_date']
    startDate = data['start_date']

    aggregationType = data['aggregation_type']
    print("aggtype", aggregationType)
    aggregationLength = data['aggregation_length']
    print("agglength", aggregationLength)
    coords = data["roi"]
    

    name, dates, paths, col, zipPath, gifPath, jpegPaths = webGeneratePaths(coords, (ee.Date(str(startDate)), ee.Date(str(endDate))), imageType, aggregationLength, aggregationType, 100)
    
    print(dates)
    print(type(dates))
    #gifPath = create_gif(paths, name, dates)
    currentData = (name, dates, paths, col)
    roi = coordsToROI(coords).bounds(10)
    boundsGeom = roi.getInfo()['coordinates']

    coordFrame = pd.DataFrame(boundsGeom[0], columns=["Lat", 'Lon'])
    s = min(coordFrame['Lat'])
    n = max(coordFrame['Lat'])
    w = min(coordFrame['Lon'])
    e = max(coordFrame['Lon'])

    sw = (s,w)
    ne = (n,e)

    response = jsonify(name=name, dates=dates, s=s, e=e, w=w, n=n, gifUrl=gifPath, zipUrl=zipPath, tifPaths = paths, x=paths)

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@app.route('/api/mapping/download', methods=['GET'])
def serveZip():
    if zipPayload!= None:
        pass
    else:
        name, dates, paths, col = currentData

