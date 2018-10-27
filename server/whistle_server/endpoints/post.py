from flask_restful import abort, Resource
from flask import request, g
from flask.json import jsonify

class PostEndpoint(Resource):
    def get(self, post_id):
        return {}, 200