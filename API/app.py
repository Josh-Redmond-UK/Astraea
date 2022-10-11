from flask import Flask
from flask import request, jsonify
from src import utils
import ee

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

    imageType = request.args['ImageType']

    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."



    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return str(id * 100)
