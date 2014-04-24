from app import app
from flask import render_template
import os
image_dir = 'app/static/images/'

@app.route('/')
def index():
	images = set(os.listdir(image_dir))
	print images
	return render_template('wall.html', images = images)

@app.route('/upload', methods = ['GET'])
def upload():
	return render_template('wall.html')
