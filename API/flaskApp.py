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
    
    gif_url = f"/gif?path={response['GifUrl']}"
    png_urls = [f"/png?path={path}" for path in response['ImgUrls']]

    # Send the GIF file
    return jsonify({"gif_url": gif_url,
        "png_urls": png_urls})


@app.route('/api/stats', methods=['GET'])
def get_stats():
    global last_analysis_result
    if last_analysis_result is None:
        return jsonify({"error": "No analysis has been run yet"}), 404
    
    return jsonify({
        "Stats": last_analysis_result['Stats'],
        "ImgUrls": last_analysis_result['ImgUrls']
    })

@app.route('/api/png', methods=['GET'])
def serve_png():
    png_path = request.args.get('path')
    return send_file(png_path, mimetype='image/png')

@app.route('/api/gif', methods=['GET'])
def serve_gif():
    gif_path = request.args.get('path')
    return send_file(gif_path, mimetype='image/gif')

@app.route('/api/zip', methods=['GET'])
def serve_zip():
    zip_path = request.args.get('path')
    return send_file(zip_path, mimetype='application/zip')


@app.route('/api/mapping/download', methods=['GET'])
def serveZip():
    if zipPayload!= None:
        pass
    else:
        name, dates, paths, col = currentData

