#!/bin/python
import os
from flask import Flask, g, request
from flask_restful import Api

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

mongo = Pymongo()

def make_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_key',
        MONGO_URI = os.environ.get('DATABASE_URL') or 'mongodb://localhost:27017/whistle'
    )

    mongo.init_app(app)
    api = Api(app)

    return app