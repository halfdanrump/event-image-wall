from app import flapp, socketio
from flask import render_template, request
import os
from flask.ext.socketio import emit
import time
import uuid
from os.path import join as pathjoin

from app import rcon
def get_wall_images():
	return rcon.lrange(flapp.config['REDIS_WALL_Q'], 0, flapp.config['N_WALLPICS'])

def add_image_to_wall_q(new_image_path):
	rcon.rpush(flapp.config['REDIS_WALL_Q'], new_image_path)
	if rcon.llen(flapp.config['REDIS_WALL_Q']) < flapp.config['N_WALLPICS']:
		rcon.rpush(flapp.config['REDIS_ALL_Q'], new_image_path)
	else:
		rcon.rpush(flapp.config['REDIS_ALL_Q'], rcon.lpop(flapp.config['REDIS_WALL_Q']))


@flapp.route('/')
def index():
	images = get_wall_images()
	socketio.emit('images',
					{'images':images},
					namespace = '/test')

	return render_template('wall.html')

@flapp.route('/newwall')
def newwall():
	images = get_wall_images()
	socketio.emit('images',
					{'images':images},
					namespace = '/test')

	return render_template('wall2.html', cd = {(1,1): 'dog.jpg', (5,5):'animal.jpg'})
	

@flapp.route('/upload', methods = ['POST'])
def upload():
	# save received image to /static/images
	# emit event to client telling it to append images
	new_image_path = pathjoin(flapp.config['IMAGE_UPLOAD_DIR'], uuid.uuid4().hex)

	print 'Saving image to %s'%new_image_path
	f = open(new_image_path, 'w')
	f.write(request.data)
	f.close()

	if flapp.config['DISPLAY_MODE'] == 'queue':
		add_image_to_wall_q(new_image_path)
		images = map(lambda x: '/'.join(x.split('/')[1::]), get_wall_images())

		socketio.emit('images',
						{'images':images},
						namespace = '/test')

	

	return render_template('wall.html')


@socketio.on('request images', namespace = '/test')
def send_images():
	images = map(lambda x: '/'.join(x.split('/')[1::]), get_wall_images())
	print images
	socketio.emit('images',
				{'images':images},
				namespace = '/test')


