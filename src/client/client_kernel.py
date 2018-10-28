import requests

url = "https://whistle-hackohio.herokuapp.com"


class ClientKernel:
    def __init__(self, app):
        self.kernel_thread = None
        self.cookies = None
        self.app = app

    def login(self, username: str, password: str):
        data = {
            "username": username,
            "password": password,
        }
        r = requests.post(url + "/login", json=data)
        if r.status_code == 201:
            self.cookies = r.cookies
        self.app.response = r

    def register(self, username: str, password: str):
        data = {
            "username": username,
            "password": password,
        }
        r = requests.post(url + "/user/create", json=data)
        self.app.response = r

    def logoff(self):
        self.cookies = None
