#!/usr/bin/python3
"""first api with flask and python"""

from flask import Flask, jsonify
from flask_cors import CORS  # allow cross origin
from models import storage
from api.v1.views import app_views
from os import getenv
from flasgger import Swagger


app = Flask('v1')
Swagger(app)  # allow swagger

app.register_blueprint(app_views)
CORS(app, resources=r"/api/v1/*", origins="*")
app.url_map.strict_slashes = False # allow /api/v1/states/ and /api/v1/states
host = getenv('HBNB_API_HOST')
port = getenv('HBNB_API_PORT')
threaded = True if getenv('HBNB_API_HOST') else False

@app.errorhandler(404)
def error(self):
    """404 error but return empty dict"""
    return jsonify({"error": "Not found"}), 404

@app.teardown_appcontext
def teardown(*args, **kwargs):
    """close storage"""
    storage.close()

#allow cross origin for all routes and methods
@app.after_request  # after request
def after_request(response):
    """allow cross origin for all routes and methods"""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
    response.headers['Accept'] = '*/*'
    return response


if __name__ == "__main__":
    if host is None:
        HBNB_API_HOST = '0.0.0.0'
    if port is None:
        HBNB_API_PORT = 5000
    print(app.url_map)
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=threaded)