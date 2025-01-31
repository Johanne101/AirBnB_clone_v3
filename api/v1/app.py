#!/usr/bin/python3
""" first endpoint for status of our API """

from flask import Blueprint, Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv


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
    HOST = getenv('HBNB_API_HOST')
    PORT = getenv('HBNB_API_PORT')
    app.run(host=HOST, port=PORT, threaded=True)
