from app import flapp, socketio
from flask import render_template, request
import os
from flask.ext.socketio import emit
import time
import uuid
from os.path import join as pathjoin
from random import sample
from app import rcon

def get_queue_wall_images():
	return rcon.lrange(flapp.config['REDIS_WALL_Q'], 0, flapp.config['N_QUEUE_WALLPICS'] + 1)


def add_image_to_wall_q(new_image_path):
	rcon.rpush(flapp.config['REDIS_WALL_Q'], new_image_path)
	
	if rcon.llen(flapp.config['REDIS_WALL_Q']) < flapp.config['N_QUEUE_WALLPICS']:
		rcon.rpush(flapp.config['REDIS_ALL_Q'], new_image_path)
	else:
		rcon.rpush(flapp.config['REDIS_ALL_Q'], rcon.lpop(flapp.config['REDIS_WALL_Q']))


def store_pic(new_image_path, request):
	f = open(new_image_path, 'w')
	f.write(request.data)
	f.close()


################################
### Handlers routes
##################################


@flapp.route('/queue')
def queuewall():
	previous_images = set(os.listdir(flapp.config['QUEUE_DIR']))
	previous_images = map(lambda f: flapp.config['QUEUE_DIR'] + f, previous_images) 
	for img in previous_images:
		add_image_to_wall_q(img)
	images = get_queue_wall_images()
	print images
	socketio.emit('images', {'images':images}, namespace = '/queue')
	return render_template('queue.html')

import random
@flapp.route('/')
def static_wall():
	images = set(os.listdir(flapp.config['QUEUE_DIR']))
	images = map(lambda f: flapp.flaskify(flapp.config['QUEUE_DIR'] + f), images) 
	images = random.sample(images, len(images))
	print images
	return render_template('static_wall.html', images = images)


@flapp.route('/random')
def randomwall():
	return render_template('random.html')


@flapp.route('/grid_white')
def grid_white():
	return render_template('grid_white.html', n_rows = 3, n_columns = 5, image_size = 350)

@flapp.route('/grid_sketch')
def grid_sketch():
	return render_template('grid_sketch.html', n_rows = 3, n_columns = 5, image_size = 350)

@flapp.route('/grid_black')
def grid_black():
	return render_template('grid_black.html', n_rows = 3, n_columns = 5, image_size = 350)


@flapp.route('/grid_crazy')
def grid_crazy():
	return render_template('grid_crazy.html', n_rows = 10, n_columns = 5, image_size = 350)



################################
### Handlers for uploading images
##################################

@flapp.route('/upload_queue_image', methods = ['POST'])
def handle_queue_image():
	def get_random_cell():
		return '%s_%s'%(sample(range(flapp.config['N_GRID_ROWS']), 1)[0], sample(range(flapp.config['N_GRID_COLUMNS']), 1)[0])

	new_image_path = pathjoin(flapp.config['QUEUE_DIR'], uuid.uuid4().hex)
	store_pic(new_image_path, request)
	add_image_to_wall_q(new_image_path)
	images = map(lambda x: '/'.join(x.split('/')[1::]), get_queue_wall_images())
	socketio.emit('images', {'images':images, 'cell':get_random_cell()}, namespace = '/queue')	
	return render_template('queue.html')


@flapp.route('/upload_random_image', methods = ['POST'])
def handle_random_image():
	new_image_path = pathjoin(flapp.config['RANDOM_DIR'], uuid.uuid4().hex)
	store_pic(new_image_path, request)
	return render_template('random.html')


@flapp.route('/upload_grid_image_white', methods = ['POST'])
def handle_grid_image_white():
	new_image_path = pathjoin(flapp.config['GRID_DIR_WHITE'], uuid.uuid4().hex)
	store_pic(new_image_path, request)
	return render_template('dummy.html')


@flapp.route('/upload_grid_image_black', methods = ['POST'])
def handle_grid_image_black():
	new_image_path = pathjoin(flapp.config['GRID_DIR_BLACK'], uuid.uuid4().hex)
	store_pic(new_image_path, request)
	return render_template('dummy.html')


@flapp.route('/upload_grid_image_sketch', methods = ['POST'])
def handle_grid_image_sketch():
	new_image_path = pathjoin(flapp.config['GRID_DIR_SKETCH'], uuid.uuid4().hex)
	store_pic(new_image_path, request)
	return render_template('dummy.html')


###################
# Event handlers for when client requests images
##################

@socketio.on('request images', namespace = '/grid')
def send_images():
	flapp.logger.debug('Got images request in namespace: grid')


@socketio.on('request images', namespace = '/queue')
def send_queue_images():
	flapp.logger.debug('Got images request in namespace: queue')
	images = map(lambda x: '/'.join(x.split('/')[1::]), get_queue_wall_images())
	socketio.emit('images',	{'images':images}, namespace = '/queue')


@socketio.on('request images', namespace = '/random')
def send_random_images():
	flapp.logger.debug('Got images request in namespace: random')
	# images = map(lambda x: '/'.join(x.split('/')[1::]), get_queue_wall_images())
	# print images
	# socketio.emit('images',	{'images':images}, namespace = '/test')


