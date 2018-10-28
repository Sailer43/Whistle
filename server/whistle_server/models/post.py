from whistle_server import mongo
from bson.objectid import ObjectId

class Post:
    def __init__(self, obj):
        self.obj = obj

    @staticmethod
    def find_by_id(post_id):
        return Post.find_by_object_id(ObjectId(post_id))

    @staticmethod
    def find_by_object_id(object_id):
        post = mongo.db.posts.find_one({"_id": object_id})
        if post is None:
            return None
        return Post(post)

    @staticmethod
    def create(user_id, text, window_id):
        obj = {}
        obj["author_id"] = ObjectId(user_id)
        obj["text"] = text
        obj["window_id"] = ObjectId(window_id)
        obj["comments"] = []
        obj["published"] = False
        obj["rating"] = 0
        post = mongo.db.posts.insert_one(obj)
        post = mongo.db.posts.find_one({"_id": post.inserted_id})
        if post is None:
            return None
        return Post(post)

    def reload(self):
        self.obj = mongo.db.posts.find_one({"_id":self.obj["_id"]})

    def serialize(self):
        response = self.obj
        response["post_id"] = str(self.obj["_id"])
        user = User.find_by_id(self.obj["author_id"])
        response["author_name"] = user.obj["username"]
        response["author_id"] = str(self.obj["author_id"])
        response["window_id"] = str(self.obj["window_id"])
        del response["_id"]
        return response

    @staticmethod
    def delete(post_id):
        mongo.db.posts.delete_one({"_id": ObjectId(post_id)})

from .user import User