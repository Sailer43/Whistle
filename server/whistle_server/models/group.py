from whistle_server import mongo
from bson.objectid import ObjectId

class Group:
    def __init__(self, obj):
        self.obj = obj

    @staticmethod
    def find_by_id(group_id):
        return Group.find_by_object_id(ObjectId(group_id))

    @staticmethod
    def find_by_object_id(object_id):
        group = mongo.db.groups.find_one({"_id": object_id})
        if group is None:
            return None
        return Group(group)

    @staticmethod
    def find_by_name(name):
        group = mongo.db.groups.find_one({"name": name})
        if group is None:
            return None
        return Group(group)

    @staticmethod
    def delete(group_id):
        group = mongo.db.groups.delete_one({"_id": ObjectId(group_id)})


    @staticmethod
    def create(name):
        group = Group.find_by_name(name)
        if group is not None:
            return None
        obj = {"name": name}
        obj["posts"] = []
        group = mongo.db.users.insert_one(obj)
        group = mongo.db.users.find_one({"_id": group.inserted_id})
        if group is None:
            return None
        return Group(group)

    def serialize(self):
        response = self.obj
        response["group_id"] = str(self.obj["_id"])
        del response["_id"]
        del response["posts"]
        return response