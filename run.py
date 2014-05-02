from app import app, socketio, conf, args
from threading import Thread

import os
from random import sample, gauss
import time


def random_image_daemon():
	while True:
		images = set(os.listdir(conf.resized_image_dir))
		try:
			images.remove('.DS_Store')
		except KeyError:
			pass
		images = set(map(lambda x: app.flaskify(conf.resized_image_dir) + x, images))
		selected_images = sample(images, min(conf.number_of_pictures_on_wall, len(images)))
		socketio.emit('update displayed images',
					 {'images':selected_images},
					  namespace = '/test')
		time.sleep(10)

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
	if args.behavior == 'random':
		Thread(target = random_image_daemon).start()

	socketio.run(app, port = 8080)
