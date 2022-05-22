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


if __name__ == '__main__':
    hbnb_api_host = getenv('HBNB_API_HOST')
    hbnb_api_port = getenv('HBNB_API_PORT')
    if hbnb_api_host is None and hbnb_api_port is None:
        app.run(host='0.0.0.0', port=5000, threaded=True)
    elif hbnb_api_host is None:
        app.run(host='0.0.0.0', port=api_port, threaeded=True)
    elif hbnb_api_port is None:
        app.run(host=api_host, port=5000, threaded=True)
    else:
        app.run(host=api_host, port=api_port, threaded=True)
