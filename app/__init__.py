import argparse
parser = argparse.ArgumentParser(description = 'Run as main to start the Event Image Wall app server')
parser.add_argument('-p', '--production', help = 'Set production environment', action = "store_true")
parser.add_argument('-b', '--behavior', help = 'Specify how images are displayed on the wall', choices = ('queue', 'random'), default = 'queue')
args = parser.parse_args()


from flask import Flask
app = Flask(__name__)

if args.production:
	app.config.from_object('app.conf.Production')
else:
	app.config.from_object('app.conf.Development')
import redis
rcon = redis.Redis()

from app.conf import *

from flask.ext.socketio import SocketIO
socketio = SocketIO(app)

def flaskify(path):
	return path.replace('app', '')

app.flaskify = flaskify
from app import views, conf, args, parser