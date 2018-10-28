import os
import tempfile
import pytest
import time
from .context import make_app, mongo, User, Window, Group

class TestUser:
    def setup(self):
        self.user = User.create("pytest", "pytest")
        self.group = Group.create("name")
        if self.user is None:
            self.user = User.find_by_username("pytest")
        self.window = Window.create(time.time(), 1000, self.group.obj["_id"])

    def teardown(self):
        print("\nTearing down")
        User.delete(self.user.obj["_id"])
        Window.delete(self.window.obj["_id"])
        Group.delete(self.group.obj["_id"])

    def test_user_exists(self):
        user = User.find_by_username("pytest")
        assert user is not None

    def test_find_by_id(self):
        user = User.find_by_id(self.user.obj["_id"])
        assert user is not None

    def test_find_by_username(self):
        user = User.find_by_username(self.user.obj["username"])
        assert user is not None

    def test_has_no_window_then_does(self):
        assert not self.user.has_window(self.window.obj["_id"])
        self.user.add_window(self.window.obj["_id"])
        assert self.user.has_window(self.window.obj["_id"]) == True
        self.user.remove_window(self.window.obj["_id"])
        assert not self.user.has_window(self.window.obj["_id"])

    def test_detects_active(self):
        self.user.add_window(self.window.obj["_id"])
        assert self.user.in_window()
        self.user.remove_window(self.window.obj["_id"])


class TestWindow:
    def setup(self):
        self.user = User.create("pytest", "pytest")
        self.group = Group.create("name")
        if self.user is None:
            self.user = User.find_by_username("pytest")
        self.window = Window.create(time.time(), 1000, self.group.obj["_id"])

    def teardown(self):
        print("\nTearing down")
        User.delete(self.user.obj["_id"])
        Window.delete(self.window.obj["_id"])
        Group.delete(self.group.obj["_id"])

    def test_add_user(self):
        assert len(self.window.obj["users"])==0
        assert self.window.add_user(self.user.obj["_id"])
        assert len(self.window.obj["users"])==1
        assert self.window.remove_user(self.user.obj["_id"])
        assert len(self.window.obj["users"])==0


