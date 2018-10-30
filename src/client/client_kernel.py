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

    def get_general_post(self):
        r = requests.get(url + "/posts")
        self.app.response = r

    def get_single_post(self, post_id: str):
        r = requests.get(url + "/post/" + post_id)
        self.app.response = r

    def get_own_page(self):
        r = requests.get(url + "/user", cookies=self.cookies)
        self.app.response = r

    def get_conditional_post(self, group_id):
        r = requests.get(url + "/posts/" + group_id)
        self.app.response = r

    def publish_post(self, text: str, window_id: str):
        data = {
            "text": text,
            "window_id": window_id,
        }
        r = requests.post(url + "/post", json=data, cookies=self.cookies)
        self.app.response = r

    def fetch_user(self):
        r = requests.get(url + "/user", cookies=self.cookies)
        return r
