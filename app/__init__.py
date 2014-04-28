from flask import Flask
app = Flask(__name__)
app.config.update(
	DEBUG = True,
	PROPAGATE_EXCEPTIONS = True
	)


from app.conf import *

from flask.ext.socketio import SocketIO
socketio = SocketIO(app)

def flaskify(path):
	return path.replace('app', '')

app.flaskify = flaskify
from app import views