from flask_restful import abort, Resource
from flask import request, g
from flask.json import jsonify

class GetPostsEndpoint(Resource):
    def get(self, group_id=0):
        return {}, 200