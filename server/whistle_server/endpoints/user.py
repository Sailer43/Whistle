from flask_restful import abort, Resource
from flask import request, g, session
from flask.json import jsonify
from whistle_server.models.post import Post
from whistle_server.models.window import Window
from whistle_server.models.group import Group
from whistle_server.models.user import User

class UserEndpoint(Resource):
    def get(self, user_id=None):
        if user_id is None:
            if not session or "_session" not in session or not session["_session"]:
                abort(401)
            user_id = session["_session"]
        user = User.find_by_id(user_id)
        if user is None:
            abort(401)
        response = user.serialize()
        print(response)
        response = jsonify(response)
        response.status_code = 200
        return response

    def post(self, user_id=None):
        return self.get(user_id)