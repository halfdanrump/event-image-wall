from app import app, socketio
from threading import Thread

import os
from random import sample, gauss
import time



def random_image_daemon():
	while True:
		images = set(os.listdir(app.config['RESIZED_IMAGE_DIR']))
		try:
			images.remove('.DS_Store')
		except KeyError:
			pass
		images = set(map(lambda x: app.flaskify(app.config['RESIZED_IMAGE_DIR']) + x, images))
		selected_images = sample(images, min(app.config['N_WALLPICS'], len(images)))
		
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
	import argparse
	parser = argparse.ArgumentParser(description = 'Run as main to start the Event Image Wall app server')
	parser.add_argument('-p', '--production', help = 'Set production environment', action = "store_true")
	parser.add_argument('-b', '--behavior', help = 'Specify how images are displayed on the wall', choices = ('queue', 'random'), default = 'queue')
	args = parser.parse_args()	

	if args.production:
		app.config.from_object('conf.Production')
	else:
		app.config.from_object('conf.Development')

	if args.behavior == 'random':
		Thread(target = random_image_daemon).start()

	socketio.run(app, port = 8080)
