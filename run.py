from app import flapp, socketio
from threading import Thread

import os
import shutil
from random import sample, gauss
import time
import argparse


def random_image_daemon():
	while True:
		images = set(os.listdir(flapp.config['IMAGE_UPLOAD_DIR']))
		try:
			images.remove('.DS_Store')
		except KeyError:
			pass
		images = set(map(lambda x: flapp.flaskify(flapp.config['IMAGE_UPLOAD_DIR']) + x, images))
		selected_images = sample(images, min(flapp.config['N_WALLPICS'], len(images)))
		
		print selected_images
		socketio.emit('update wall pics',
					 {'images':selected_images},
					  namespace = '/test')
		time.sleep(5)

if __name__ == "__main__":

	"""
	In image monitor on camera laptop: 
		- Move image to uploaded folder when it has been uploaded
	In image monitor on server: 
		- Main list of all received images in redis
			- 
		- Maintain set/list of currently showed pictures in redis
			- GET request fetches list
			- socket event new_image modifies list and pushes the list to clients

	"""
	
	parser = argparse.ArgumentParser(description = 'Run as main to start the Event Image Wall app server')
	parser.add_argument('-p', '--production', help = 'Set production environment', action = "store_true")
	parser.add_argument('-b', '--behavior', help = 'Specify how images are displayed on the wall', choices = ('queue', 'random'), default = 'queue')
	parser.add_argument('--delete-old-images', action = "store_true")
	args = parser.parse_args()	

	from app.conf import Production, Development
	if args.production:
		config = Production(behavior = args.behavior)
	else:
		config = Development(behavior = args.behavior)

	flapp.config.from_object(config)

	if args.delete_old_images:
		print 'Deleting old images'
		shutil.rmtree(flapp.config['IMAGE_UPLOAD_DIR'])
		os.makedirs(flapp.config['IMAGE_UPLOAD_DIR'])
		


	if args.behavior == 'random':
		Thread(target = random_image_daemon).start()
	
	socketio.run(flapp, port = 8080)
