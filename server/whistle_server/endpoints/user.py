from flask_restful import abort, Resource
from flask import request, g
from flask.json import jsonify

class UserEndpoint(Resource):
    def get(self, user_id):
        return {}, 200