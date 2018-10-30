from whistle_server import mongo
from bson.objectid import ObjectId
# from whistle_server.models.window import Window
import time

def hash_password(password):
    from werkzeug.security import generate_password_hash
    return generate_password_hash(password)

class User:
    """
    Deals with the model of User
    Methods:
        in_window
        has_window
        add_post
        remove_post
        add_window
        remove_window
        reload
        find_by_username
        find_by_id
    """
    def __init__(self, obj):
        self.obj = obj

    def in_window(self):
        # from whistle_server.models.window import Window

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
        # from whistle_server.models.window import Window
        print("Im here")
        window = Window.find_by_id(window_id)
        print("Got window")
        print(window)
        if window is None:
            return
        print("Found window")
        windows = self.obj["windows"]
        window_id = ObjectId(window_id)
        return window_id in windows

    def add_post(self, post_id):
        mongo.db.users.update_one({"_id":self.obj["_id"]},
            {"$push": {"posts":ObjectId(post_id)}})
        self.reload()
        return True

    def remove_post(self, post_id):
        mongo.db.users.remove_one({"_id":self.obj["_id"]},
            {"$pull": {"posts":vObjectId(post_id)}})
        self.reload()
        return True


    def add_window(self, window_id):
        if self.has_window(window_id):
            return None
        mongo.db.users.update_one({"_id":self.obj["_id"]},
            {"$push": {"windows":ObjectId(window_id)}})
        self.reload()
        return True

    def remove_window(self, window_id):
        mongo.db.users.update_one({"_id":self.obj["_id"]},
            {"$pull": {"windows": ObjectId(window_id)}})
        self.reload()
        return True

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
        return User.find_by_object_id(ObjectId(user_id))

    @staticmethod
    def find_by_object_id(user_id):
        user = mongo.db.users.find_one({"_id": user_id})
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
        obj["groups"] = [ObjectId("5bd5609cfc31dabe575fe2cd")]
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

    @staticmethod
    def sample_in_group(group_id, n):
        return mongo.db.users.aggregate([
            { "$sample": {"size": n} },
            { "$match":  {"group_id": group_id} }
        ])

    def set_half(self):
        mongo.db.posts.update_one({"_id": self.obj["_id"]},
            {"$set":{"half": True}})
        self.reload()


    def serialize(self):
        response = self.obj
        print(response)
        response["user_id"] = str(response["_id"])
        del response["_id"]
        del response["password_hash"]
        print(response)
        posts = []
        for post_id in response["posts"]:
            post = Post.find_by_object_id(post_id)
            if post is not None:
                posts.append(post.serialize())
        response["posts"] = posts

        windows = []
        for window_id in response["windows"]:
            window = Window.find_by_object_id(window_id)
            if window is not None:
                windows.append(window.serialize())
        response["windows"] = windows

        groups = []
        for group_id in response["groups"]:
            print(group_id)
            group = Group.find_by_object_id(group_id)
            print(group)
            if group is not None:
                groups.append(group.serialize())
        print(groups)
        response["groups"] = groups
        return response

from .group import Group
from .window import Window
from .post import Post
