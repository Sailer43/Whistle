import os
import tempfile
import pytest
import time
from flask import session
from .context import make_app, mongo, User, Window, Post, Group
import requests

class TestUser:
    def setup(self):
        self.group = Group.create("name")
        self.user = User.create("pytest", "pytest")
        if self.user is None:
            self.user = User.find_by_username("pytest")
        self.window = Window.create(time.time(), 1000, self.group.obj["_id"])

    def teardown(self):
        print("\nTearing down")
        User.delete(self.user.obj["_id"])
        Window.delete(self.window.obj["_id"])
        Group.delete(self.group.obj["_id"])

    def test_add_post(self):
        app = make_app()
        with app.test_client() as c:
            # cehck window has no posts
            assert len(self.window.obj["posts"])==0

            data = c.post('/login',json={"username":"pytest","password":"pytest"})
            # log in
            session["_session"] = str(User.find_by_username("pytest").obj["_id"])

            # post to existent, but not assigned window
            post = c.post('/post', json={"window_id":str(self.window.obj["_id"]),
                "text": "stuff"})
            assert post.status == "404 NOT FOUND"
            # assign window
            self.user.add_window(self.window.obj["_id"])
            # post to open window
            post = c.post('/post', json={"window_id":str(self.window.obj["_id"]),
                "text": "stuff"})
            assert post.status == "200 OK"
            self.window.reload()
            # check that post exists
            assert len(self.window.obj["posts"])==1
            Post.delete(post.json["post_id"])
            # make sure the window is gone from user
            post = c.post('/post', json={"window_id":str(self.window.obj["_id"]),
                "text": "stuff"})
            assert post.status == "404 NOT FOUND"
