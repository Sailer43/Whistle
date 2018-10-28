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
                    "users": ObjectId(user_id)
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
            {"$pull": {"posts":ObjectId(post_id)}})
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
    def create(start_time, duration, group_id):
        obj = {}
        obj["start_time"] = start_time
        obj["duration"] = duration
        obj["publish_time"] = start_time + duration
        obj["group_id"] = ObjectId(group_id)
        obj["users"] = []
        obj["posts"] = []
        window = mongo.db.windows.insert_one(obj)
        window = mongo.db.windows.find_one({"_id": window.inserted_id})
        if window is None:
            return None
        return Window(window)

    def serialize(self):
        response = self.obj
        group = Group.find_by_object_id(self.obj["group_id"])
        response["group"] = group.obj["name"]
        response["group_id"] = str(response["group_id"])
        response["window_id"] = str(self.obj["_id"])
        del response["_id"]
        del response["users"]
        del response["posts"]
        return response

    @staticmethod
    def delete(window_id):
        mongo.db.windows.delete_one({"_id": ObjectId(window_id)})

    @classmethod
    def find_soonest_in_group(group_id):
        return Window(mongo.db.windows.find({"group_id": group_id}, sort=[("start_time", 1)]))

from .user import User