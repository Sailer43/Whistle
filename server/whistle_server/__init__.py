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
    app.debug = True

    mongo.init_app(app)
    api = Api(app)

    from .endpoints.user import UserEndpoint
    from .endpoints.login import LoginEndpoint, CreateUserEndpoint
    from .endpoints.post import GetPostEndpoint, CreatePostEndpoint
    from .endpoints.posts import GetPostsEndpoint
    from .endpoints.scheduler import SchedulerEndpoint

    api.add_resource(UserEndpoint, '/user', '/user/<string:user_id>', endpoint="user")
    api.add_resource(CreateUserEndpoint, '/user/create', endpoint="create_user")
    api.add_resource(LoginEndpoint, '/login', endpoint="login")
    api.add_resource(GetPostEndpoint, '/post/<string:post_id>', endpoint="post")
    api.add_resource(GetPostsEndpoint, '/posts/<string:group_id>', '/posts', endpoint="posts")
    api.add_resource(CreatePostEndpoint, '/post', endpoint="create_post")
    api.add_resource(SchedulerEndpoint, '/schedule', endpoint="scheduler")

    return app