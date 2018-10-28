from whistle_server import mongo
from bson.objectid import ObjectId
import time

class Window:

    def __init__(self, obj):
        self.obj = obj

    def is_active(self):
        now = time.time()
        if now >= self.obj["start_time"] and now < self.obj["publish_time"]:
            return True
        else:
            return False

    def add_user(self, user_id):
        # from whistle_server.models.user import User

        user = User.find_by_id(user_id)
        if not user:
            return False
        user.add_window(self.obj["_id"])

        mongo.db.windows.update_one({"_id":self.obj["_id"]},
            {"$push": {"users":ObjectId(user_id)}})
        self.reload()
        return True

    def remove_user(self, user_id):
        # from whistle_server.models.user import User

        user = User.find_by_id(user_id)
        if not user:
            return False
        user.remove_window(self.obj["_id"])

        mongo.db.windows.update_one({"_id":self.obj["_id"]},
            {
                "$pull": {
                    "users": {
                            "_id": ObjectId(user_id)
                    }
                }
            })
        self.reload()
        return True

    def add_post(self, post_id):
        mongo.db.windows.update_one({"_id":self.obj["_id"]},
            {"$push": {"posts":ObjectId(post_id)}})
        self.reload()
        return True

    def remove_post(self, post_id):
        mongo.db.windows.remove_one({"_id":self.obj["_id"]},
            {"$pull": {"posts":{"_id":ObjectId(post_id)}}})
        self.reload()
        return True

    def reload(self):
        self.obj = mongo.db.windows.find_one({"_id":self.obj["_id"]})

    @staticmethod
    def find_by_id(window_id):
        return Window.find_by_object_id(ObjectId(window_id))

    @staticmethod
    def find_by_object_id(object_id):
        window = mongo.db.windows.find_one({"_id": object_id})
        if window is None:
            return None
        return Window(window)

    @staticmethod
    def create(start_time, duration):
        obj = {}
        obj["start_time"] = start_time
        obj["duration"] = duration
        obj["publish_time"] = start_time + duration
        obj["users"] = []
        obj["posts"] = []
        window = mongo.db.windows.insert_one(obj)
        window = mongo.db.windows.find_one({"_id": window.inserted_id})
        if window is None:
            return None
        return Window(window)

    def serialize(self):
        response = self.obj
        response["window_id"] = str(self.obj["_id"])
        del response["_id"]
        del response["users"]
        del response["posts"]
        return response

    @staticmethod
    def delete(window_id):
        mongo.db.windows.delete_one({"_id": ObjectId(window_id)})


from .user import User