#!/usr/bin/python3


from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_storage(exception):
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    hbnb_api_host = getenv('HBNB_API_HOST')
    hbnb_api_port = getenv('HBNB_API_PORT')
    if hbnb_api_host is None:
        hbnb_api_host = '0.0.0.0'
    if hbnb_api_port is None:
        hbnb_api_port = '5000'
        app.run(hbnb_api_host, hbnb_api_port, threaded=True)
