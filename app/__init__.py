from flask import Flask
app = Flask(__name__)

from app.config import *

from flask.ext.socketio import SocketIO
socketio = SocketIO(app)

def flaskify(path):
	return path.replace('app', '')

app.flaskify = flaskify
from app import views