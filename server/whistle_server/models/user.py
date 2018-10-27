from whistle_server import mongo

def hash_password(password):
    from werkzeug.security import generate_password_hash
    return generate_password_hash(password)

class User:
    def __init__(self, obj):
        self.obj = obj

    @staticmethod
    def find_by_username(username):
        user = mongo.db.users.find_one({"username": username})
        if user is None:
            return None
        return User(user)

    @staticmethod
    def find_by_id(obj):
        user = mongo.db.users.find_one({"_id": username})
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
        if user is None:
            return None
        return User(user)