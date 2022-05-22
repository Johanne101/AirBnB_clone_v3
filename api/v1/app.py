#!/usr/bin/python3


from os import getenv
from flask import Flask
from models import storage
from api.v1.views import app_views
