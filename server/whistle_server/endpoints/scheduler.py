from flask_restful import abort, Resource
from flask import request, g, session
from flask.json import jsonify
import time
import random
from math import floor
from whistle_server import mongo
from whistle_server.models.group import Group
from whistle_server.models.window import Window
from whistle_server.models.post import Post
from whistle_server.models.user import User

class SchedulerEndpoint(Resource):
    def post(self):
        now = time.time()
        groups = mongo.db.groups.find({})

        for group in groups:
            process_group(Group(group), now)


def process_group(group, now):
    interval = group.obj["interval"]
    window = Window.find_soonest_in_group(group.obj["_id"])
    print(window)
    if window is None:
        Window.create(now, interval, group.obj["_id"])
    if window.obj["start_time"] > now:
        return
    # it's the same of equal, so it's time to pick
    if window.obj["publish_time"] <= now:
        choose_and_post(window, group)
    else:
        if len(window.obj["users"]) == 0:
            add_users(window, group)
            Window.create(now, interval, group.obj["_id"])
        else:
            # additionally
            user_ids = window.obj["users"]
            if(len(user_ids)==0):
                return
            user = User.find_by_object_id(user_ids[0])
            if "half" not in user.obj:
                add_users(window, group)
                for user_id in user_ids:
                    user = User.find_by_object_id(user_id)
                    if user is not None:
                        user.set_half()

def choose_and_post(window, group):
    posts = window.obj["posts"]
    if len(posts)==0:
        return False # no submissions
    chosen_post_id = posts[floor(random.random()*len(posts))]
    chosen_post = Post.find_by_object_id(chosen_post_id)
    chosen_post.publish()
    group.add_post(chosen_post_id)
    for user_id in window.obj["users"]:
        user = User.find_by_object_id(user_id)
        user.remove_window(window.obj["_id"])



def add_users(window, group):
    users = User.sample_in_group(group.obj["_id"], 5)
    for user_id in users:
        window.add_user(user_id)
