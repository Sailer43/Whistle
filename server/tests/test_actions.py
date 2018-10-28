import os
import tempfile
import pytest
import time
from .context import make_app, mongo, User, Window, Post, Group

class TestUser:
    def setup(self):
        self.user = User.create("pytest", "pytest")
        if self.user is None:
            self.user = User.find_by_username("pytest")
        self.window = Window.create(time.time(), 1000)

    def teardown(self):
        print("\nTearing down")
        User.delete(self.user.obj["_id"])
        Window.delete(self.window.obj["_id"])

    def test_add_post(self):
        with app.test_client() as c:
            pass