from src.utils import *
from src.api_utils import handle_request
from flask import Flask, send_file, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

ee.Initialize()

global currentData
global zipPayload
global activeCollection

last_analysis_result = None

@app.route('/api/mapping', methods=['GET'])
def generate_paths():
    global last_analysis_result
    data = json.loads(request.args['params'])
    clean_up_wd()
    response = handle_request(data)
    
    # Store the full response for the stats endpoint
    last_analysis_result = response
    
    # Send the GIF file
    return send_file(response['GifUrl'], mimetype='image/gif')

@app.route('/api/stats', methods=['GET'])
def get_stats():
    global last_analysis_result
    if last_analysis_result is None:
        return jsonify({"error": "No analysis has been run yet"}), 404
    
    return jsonify({
        "Stats": last_analysis_result['Stats'],
        "ImgUrls": last_analysis_result['ImgUrls']
    })


@app.route('/api/mapping/download', methods=['GET'])
def serveZip():
    if zipPayload!= None:
        pass
    else:
        name, dates, paths, col = currentData

