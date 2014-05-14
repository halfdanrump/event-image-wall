from app import flapp, socketio
from threading import Thread

import os
import shutil
from random import sample, gauss
import time
import argparse
from app import rcon
from app.views import add_image_to_wall_q
from random import sample


def scan_image_folder(folder):
	image_names = set(os.listdir(folder))
	try:
		image_names.remove('.DS_Store')
	except KeyError:
		pass
	images = set(map(lambda x: flapp.flaskify(folder) + x, image_names))
	return images	


def random_image_daemon():
	while True:
		images = scan_image_folder(flapp.config['RANDOM_DIR'])
		selected_images = sample(images, min(flapp.config['N_RANDOM_WALLPICS'], len(images))) 
		socketio.emit('update wall pics', {'images':selected_images}, namespace = '/random')
		time.sleep(flapp.config['WALL_REFRESH_RATE'])


def grid_image_daemon():
	while True:
		images = scan_image_folder(flapp.config['GRID_DIR'])
		selected_images = sample(images, min(1, len(images))) 
		socketio.emit('update wall pics', {'images':selected_images, 'cell':'%s_%s'%(sample(range(4), 1)[0], sample(range(8), 1)[0])}, namespace = '/grid')
		time.sleep(flapp.config['WALL_REFRESH_RATE'])


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = 'Run as main to start the Event Image Wall app server')
	parser.add_argument('-p', '--production', help = 'Set production environment', action = "store_true")
	parser.add_argument('--delete-old-images', action = "store_true")
	parser.add_argument('-r', '--wall-refresh-rate', type = int, default = 5)
	args = parser.parse_args()	

	from app.conf import Production, Development
	if args.production:
		config = Production(wall_refresh_rate = args.wall_refresh_rate)
	else:
		config = Development(wall_refresh_rate = args.wall_refresh_rate)

	flapp.config.from_object(config)

	rcon.delete(flapp.config['REDIS_WALL_Q'])
	rcon.delete(flapp.config['REDIS_ALL_Q'])
	
	
	if args.delete_old_images:
		print 'Deleting old images'
		shutil.rmtree(flapp.config['IMAGE_UPLOAD_DIR'])
		os.makedirs(flapp.config['IMAGE_UPLOAD_DIR'])
		

	Thread(target = random_image_daemon).start()
	Thread(target = grid_image_daemon).start()
	socketio.run(flapp, port = 8080)
