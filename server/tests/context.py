import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from whistle_server import make_app, mongo
from whistle_server.models.user import User
from whistle_server.models.window import Window
from whistle_server.models.post import Post

app = make_app()
mongo.init_app(app)