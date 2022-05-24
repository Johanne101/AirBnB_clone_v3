#!/usr/bin/python3
""" first endpoint for status of our API """

from os import getenv
from flask import Blueprint, Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={"/*": {"origins": ["0.0.0.0"]}})


@app.teardown_appcontext
def teardown_storage(exception):
    ''' closes storage '''
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    ''' jsonify error '''
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    ''' run api '''
    hbnb_api_host = getenv('HBNB_API_HOST')
    hbnb_api_port = getenv('HBNB_API_PORT')

    if hbnb_api_host is None:
        app.run(host='0.0.0.0', port=hbnb_api_port, threaded=True)
    elif hbnb_api_port is None:
        app.run(host=hbnb_api_host, port='5000', threaded=True)
    elif hbnb_api_host is None and hbnb_api_port is None:
        app.run(host='0.0.0.0', port='5000', threaded=True)
    else:
        app.run(host=hbnb_api_host, port=hbnb_api_port, threaded=True)
