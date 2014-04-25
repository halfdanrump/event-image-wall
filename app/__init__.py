from flask import Flask

app = Flask(__name__)


from app import views
from app.config import *

def flaskify(path):
	return path.replace('app', '')

app.flaskify = flaskify