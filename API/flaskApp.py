from src.utils import *
from src.api_utils import handle_request
from flask import Flask
from flask import request, jsonify
from flask_cors import CORS
import json

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
    data = json.loads(request.args['params'])
    print(data)
    clean_up_wd()
    print("handling request for data", data)
    response = handle_request(data)
    print("response", response)
    return response


@app.route('/api/mapping/download', methods=['GET'])
def serveZip():
    if zipPayload!= None:
        pass
    else:
        name, dates, paths, col = currentData

