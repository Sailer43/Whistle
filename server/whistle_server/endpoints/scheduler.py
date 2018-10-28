from flask_restful import abort, Resource
from flask import request, g, session
from flask.json import jsonify
from whistle_server import make_app, mongo
import time
from whistle_server.models.group import Group
from whistle_server.models.window import Window

class SchedulerEndpoint(Resource):
    def post(self):
        now = time.time()
        groups = mongo.db.groups.find({})
        for group_id in groups:
            process_group(group_id, now)


def process_group(group_id, now):
    group = Group.find_by_object_id(group_id)
    interval = group.obj["interval"]
    window = Window.find_soonest_in_group(group.obj["_id"])



