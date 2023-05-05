from utils import *
from flask import Flask
from flask import request, jsonify

app = Flask(__name__)

ee.Initialize()

global currentData
global zipPayload
global activeCollection

@app.route('/api/mapping/', methods=['GET'])
def generatePaths():
    clean_up_wd()
    zipPayload = None
    imageType = request.args['imagery-type']
    startDate = request.args['end-date']
    endDate = request.args['start-date']
    aggregationType = request.args['aggregation-type']
    aggregationLength = request.args['aggregation-length']
    coords = request.args["coords"]

    paths, name, dates = webGeneratePaths(coords, (startDate, endDate), imageType, aggregationLength, aggregationType, 100)
    currentData = (name, dates, paths)
    return jsonify(name=name, dates=dates, imagePaths=paths)


@app.route('/api/mapping/download', methods=['GET'])
def serveZip():
    if zipPayload!= None:
        foo
    else:
        name, dates, paths = currentData
