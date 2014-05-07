from app import flapp, socketio
from threading import Thread

import os
import shutil
from random import sample, gauss
import time
import argparse
from app import rcon
from app.views import add_image_to_wall_q

def random_image_daemon():
	while True:
		image_names = set(os.listdir(flapp.config['IMAGE_UPLOAD_DIR']))
		try:
			image_names.remove('.DS_Store')
		except KeyError:
			pass
		images = set(map(lambda x: flapp.flaskify(flapp.config['IMAGE_UPLOAD_DIR']) + x, image_names))
		selected_images = sample(images, min(flapp.config['N_WALLPICS'], len(images)))
		print images
		
		socketio.emit('update wall pics',
					 {'images':selected_images},
					  namespace = '/test')
		time.sleep(flapp.config['WALL_REFRESH_RATE'])

if __name__ == "__main__":

	
	parser = argparse.ArgumentParser(description = 'Run as main to start the Event Image Wall app server')
	parser.add_argument('-p', '--production', help = 'Set production environment', action = "store_true")
	parser.add_argument('-b', '--behavior', help = 'Specify how images are displayed on the wall', choices = ('queue', 'random'), required = True)
	parser.add_argument('--delete-old-images', action = "store_true")
	parser.add_argument('-r', '--wall-refresh-rate', type = int, default = 30)
	parser.add_argument('-n', '--n-wallpics', type = int, default = 20)
	args = parser.parse_args()	

	from app.conf import Production, Development
	if args.production:
		config = Production(behavior = args.behavior, wall_refresh_rate = args.wall_refresh_rate, n_wallpics = args.n_wallpics)
	else:
		config = Development(behavior = args.behavior, wall_refresh_rate = args.wall_refresh_rate, n_wallpics = args.n_wallpics)

	flapp.config.from_object(config)

	rcon.delete(flapp.config['REDIS_WALL_Q'])
	rcon.delete(flapp.config['REDIS_ALL_Q'])
	
	if args.behavior == 'queue':
		previous_images = set(os.listdir(flapp.config['IMAGE_UPLOAD_DIR']))
		previous_images = map(lambda f: flapp.config['IMAGE_UPLOAD_DIR'] + f, previous_images) 
		for img in previous_images:
			add_image_to_wall_q(img)

	if args.delete_old_images:
		print 'Deleting old images'
		shutil.rmtree(flapp.config['IMAGE_UPLOAD_DIR'])
		os.makedirs(flapp.config['IMAGE_UPLOAD_DIR'])
		



	if args.behavior == 'random':
		Thread(target = random_image_daemon).start()
	
	socketio.run(flapp, port = 8080)
