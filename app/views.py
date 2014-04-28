from app import app, socketio
from flask import render_template, request
import os
from app import conf
from flask.ext.socketio import emit
from app.conf import resized_image_dir

@app.route('/')
def index():
	print conf.resized_image_dir
	images = set(os.listdir(conf.resized_image_dir))
	try:
		images.remove('.DS_Store')
	except KeyError:
		pass
	images = set(map(lambda x: app.flaskify(conf.resized_image_dir) + x, images))
	print images
	return render_template('wall.html', images = images)

@app.route('/new', )
def new_image(images):
	print images

import uuid
@app.route('/upload', methods = ['POST'])
def upload():
	# save received image to /static/images
	# emit event to client telling it to append images
	print 'IMAGE UPLOAD'
	f = open(resized_image_dir + uuid.uuid4().hex, 'w')
	f.write(request.data)
	f.close()
	return render_template('wall.html')

@socketio.on('images', namespace = '/test')
def transfer_selected_images(image_list):
	emit('update displayed images')

