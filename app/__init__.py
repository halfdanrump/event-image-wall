from flask import Flask
app = Flask(__name__)
app.config.from_object('app.conf.Development')
import redis
rcon = redis.Redis()

from app.conf import *

from flask.ext.socketio import SocketIO
socketio = SocketIO(app)

def flaskify(path):
	return path.replace('app', '')

app.flaskify = flaskify
from app import views