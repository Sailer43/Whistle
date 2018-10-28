from flask_restful import abort, Resource
from flask import request, g, session
from flask.json import jsonify

from whistle_server.models.user import User
from whistle_server.models.window import Window
from whistle_server.models.post import Post

class GetPostEndpoint(Resource):
    def get(self, post_id):
        post = Post.find_by_id(post_id)
        if post is None:
            abort(404)
        post_data = post.serialize()
        response = jsonify(post_data)
        response.status_code = 200
        return response

class CreatePostEndpoint(Resource):
    def post(self):
        if not session or "_session" not in session or not session["_session"]:
            abort(401)
        user = User.find_by_id(session["_session"])
        if user is None:
            abort(401)
        window_id = request.json.get("window_id")
        text = request.json.get("text")
        if window_id is None or text is None:
            abort(404)
        # sanity check
        if not user.has_window(window_id):
            print("abort")
            abort(404)
        # check if it's time for the window
        window = Window.find_by_id(window_id)
        print(window)
        if not window.is_active():
            abort(404)
        post = Post.create(user.obj["_id"], text, window.obj["_id"])
        window.add_post(post.obj["_id"])
        user.add_post(post.obj["_id"])
        user.remove_window(window.obj["_id"])

        response = jsonify(post.serialize())
        response.status_code = 200
        return response


