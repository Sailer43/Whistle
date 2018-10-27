#!/bin/python
import os
from flask import Flask, g, request
from flask_restful import Api
from flask_pymongo import PyMongo

from dotenv import load_dotenv

mongo = PyMongo()

def make_app():
    basedir = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(basedir, '.env'))

    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_key',
        MONGO_URI = os.environ.get('DATABASE_URL') or 'mongodb://localhost:27017/whistle'
    )

    mongo.init_app(app)
    api = Api(app)

    from .endpoints.user import UserEndpoint
    from .endpoints.login import LoginEndpoint, CreateUserEndpoint
    from .endpoints.post import PostEndpoint
    from .endpoints.posts import PostsEndpoint

    api.add_resource(UserEndpoint, '/user/<int:user_id>', endpoint="user")
    api.add_resource(CreateUserEndpoint, '/user/create', endpoint="create_user")
    api.add_resource(LoginEndpoint, '/login', endpoint="login")
    api.add_resource(PostEndpoint, '/post/<int:post_id>', endpoint="post")
    api.add_resource(UserEndpoint, '/posts/<int:group_id>', endpoint="posts")

    return app