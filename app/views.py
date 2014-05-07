from app import flapp as app
from app import socketio
from flask import render_template, request
import os
from flask.ext.socketio import emit


@app.route('/new', )
def new_image(images):
	print images


from app import rcon
def get_wall_images():
	return rcon.lrange(app.config['REDIS_WALL_Q'], 0, app.config['N_WALLPICS'])

@app.route('/')
def index():
	images = get_wall_images()
	return render_template('wall.html')




import uuid

@app.route('/upload', methods = ['POST'])
def upload():
	# save received image to /static/images
	# emit event to client telling it to append images
	print 'IMAGE UPLOAD'
	new_image_path = app.config['IMAGE_UPLOAD_DIR'] + uuid.uuid4().hex

	rcon.rpush(app.config['REDIS_WALL_Q'], new_image_path)
	if rcon.llen(app.config['REDIS_WALL_Q']) < app.config['N_WALLPICS']:
		rcon.rpush(app.config['REDIS_ALL_Q'], new_image_path)
	else:
		rcon.rpush(app.config['REDIS_ALL_Q'], rcon.lpop(app.config['REDIS_WALL_Q']))
	images = map(lambda x: '/'.join(x.split('/')[0::]), get_wall_images())
	socketio.emit('images',
					{'images':images},
					namespace = '/test')

	
	f = open(new_image_path, 'w')
	f.write(request.data)
	f.close()
	return render_template('wall.html')


@socketio.on('request images', namespace = '/test')
def send_images():
	images = map(lambda x: '/'.join(x.split('/')[1::]), get_wall_images())
	print images
	socketio.emit('images',
				{'images':images},
				namespace = '/test')


