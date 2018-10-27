from flask_restful import abort, Resource
from flask import request, g
from flask.json import jsonify

class PostsEndpoint(Resource):
    def get(self, group_id):
        return {}, 200