from whistle_server import mongo
from bson.objectid import ObjectId

class Post:
    def __init__(self, obj):
        self.obj = obj

    @staticmethod
    def create(user_id, text, window_id):
        obj = {}
        obj["user_id"] = ObjectId(user_id)
        obj["text"] = text
        obj["window_id"] = ObjectId(window_id)
        post = mongo.db.posts.insert_one(obj)
        post = mongo.db.posts.find_one({"_id": post.inserted_id})
        if post is None:
            return None
        return Post(window)
