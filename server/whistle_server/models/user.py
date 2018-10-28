from whistle_server import mongo
from bson.objectid import ObjectId
from whistle_server.models.window import Window
import time


def hash_password(password):
    from werkzeug.security import generate_password_hash
    return generate_password_hash(password)

class User:
    def __init__(self, obj):
        self.obj = obj

    def in_window(self):
        windows = self.obj["windows"]
        window_found = False
        to_delete = []
        for i in range(len(windows)):
            window_id = windows[i]
            window = Window.find_by_object_id(window_id)
            if window is None:
                to_delete.append(i)
            else:
                if window.is_active():
                    window_found = True
        return window_found

    def has_window(self, window_id):
        window = Window.find_by_id(window_id)
        if window is None:
            return False
        windows = self.obj["windows"]
        window_id = ObjectId(window_id)
        return window_id in windows

    def add_post(self, post_id):
        mongo.db.users.update_one({"_id":self.obj["_id"]},
            {"$push": {"posts":ObjectId(post_id)}})
        self.reload()

    def remove_post(self, post_id):
        mongo.db.users.remove_one({"_id":self.obj["_id"]},
            {"$pop": {"posts":{"_id":ObjectId(post_id)}}})
        self.reload()


    def add_window(self, window_id):
        if self.has_window(window_id):
            return None
        mongo.db.users.update_one({"_id":self.obj["_id"]},
            {"$push": {"windows":ObjectId(window_id)}})
        self.reload()

    def remove_window(self, window_id):
        mongo.db.users.update_one({"_id":self.obj["_id"]},
            {"$pop": {"windows":{"_id":ObjectId(window_id)}}})
        self.reload()

    def reload(self):
        self.obj = mongo.db.users.find_one({"_id":self.obj["_id"]})

    @staticmethod
    def find_by_username(username):
        user = mongo.db.users.find_one({"username": username})
        if user is None:
            return None
        return User(user)

    @staticmethod
    def find_by_id(user_id):
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if user is None:
            return None
        return User(user)

    @staticmethod
    def create(username, password):
        user = User.find_by_username(username)
        if user is not None:
            print("user exists")
            return None
        obj = {}
        obj["username"] = username
        obj["password_hash"] = str(hash_password(password))
        obj["groups"] = []
        obj["windows"] = []
        obj["rating"] = 0
        obj["avatar_url"] = ""
        obj["posts"] = []
        user = mongo.db.users.insert_one(obj)
        user = mongo.db.users.find_one({"_id": user.inserted_id})
        if user is None:
            return None
        return User(user)

    @staticmethod
    def delete(user_id):
        mongo.db.users.delete_one({"_id": ObjectId(user_id)})