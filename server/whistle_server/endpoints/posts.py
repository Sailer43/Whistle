from flask_restful import abort, Resource
from flask import request, g
from flask.json import jsonify

from whistle_server.models.post import Post
from whistle_server.models.group import Group


class GetPostsEndpoint(Resource):
    def get(self, group_id="5bd5609cfc31dabe575fe2cd"):
        group = Group.find_by_id(group_id)
        if group is None:
            abort("404")
        posts = []
        for post_id in group.obj["posts"]:
            post = Post.find_by_object_id(post_id)
            if post is not None:
                posts.append(post.serialize())
        response = group.serialize()
        response["posts"] = posts
        response = jsonify(response)
        response.status_code = 200
        return response