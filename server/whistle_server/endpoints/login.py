from flask_restful import abort, Resource
from flask import request, g, session
from flask.json import jsonify
from whistle_server.models.user import User

def verify_password(password, hashed):
    from werkzeug.security import check_password_hash
    return check_password_hash(hashed, password)

class LoginEndpoint(Resource):
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')
        # wrong input
        if username is None or password is None:
            abort(418)
        user = User.find_by_username(username)
        # user doesn't exist
        if user is None:
            return abort(418)
        # wrong password
        if not verify_password(password, user.obj["password_hash"]):
            return abort(418)
        session["_session"] = str(user.obj['_id'])
        response = jsonify({
                "id": str(user.obj["_id"])
            })
        response.status_code = 201
        return response


class CreateUserEndpoint(Resource):
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')
        # wrong input
        if username is None or password is None:
            print('username or password is None')
            abort(418)
        user = User.create(username, password)
        if user is None:
            print('User was None')
            abort(418)
        response = jsonify({})
        response.status_code = 200
        return response