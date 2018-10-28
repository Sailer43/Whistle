from flask_restful import abort, Resource
from flask import request, g
from flask.json import jsonify

class GetPostsEndpoint(Resource):
    def get(self, group_id="0"):
        response = jsonify(
            { "posts":  [   {
                            "text": "Hey, there",
                            "author_id": "1",
                            "author_name": "Papa",
                            "rating": "12313",
                            "id": "sup"
                            },
                            {
                            "text": "stop reading those pls",
                            "author_id": "2",
                            "author_name": "Mama",
                            "rating": "32132Adas",
                            "id": "second"
                            },
                            {
                            "text": "Sitao, the system is watching you",
                            "author_id": "4",
                            "author_name": "Big Brother",
                            "rating": "12313",
                            "id": "sup"
                            },
                            {
                            "text": "JK",
                            "author_id": "42",
                            "author_name": "42Papa",
                            "rating": "12312343",
                            "id": "sup423"
                            },
                        ]
            }
        )
        response.status_code = 200
        return response