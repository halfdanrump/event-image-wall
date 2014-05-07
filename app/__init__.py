from flask import Flask
flapp = Flask(__name__)

import redis
rcon = redis.Redis()

from flask.ext.socketio import SocketIO
socketio = SocketIO(flapp)

def flaskify(path):
	return path.replace('app', '')

flapp.flaskify = flaskify
from app import views, conf