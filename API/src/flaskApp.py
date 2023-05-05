from utils import *
from flask import Flask
from flask import request, jsonify

app = Flask(__name__)

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
    currentData = (name, dates, paths, col)
    return jsonify(name=name, dates=dates, imagePaths=paths)


@app.route('/api/mapping/download', methods=['GET'])
def serveZip():
    if zipPayload!= None:
        foo
    else:
        name, dates, paths, col = currentData

