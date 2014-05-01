import argparse
parser = argparse.ArgumentParser(description = 'Run as main to start the Event Image Wall app server')
parser.add_argument('-p', '--production', help = 'Set production environment', action = "store_true")
parser.add_argument('-b', '--behavior', help = 'Specify how images are displayed on the wall', choices = ('queue', 'random'), required = True)
args = parser.parse_args()

from app import app, socketio, conf
from threading import Thread

import os
from random import sample, gauss
import time

#from tornado.wsgi import WSGIContainer
#from tornado.httpserver import HTTPServer
#from tornado.ioloop import IOLoop

# def image_monitor2():
# 	processed_images = set()
# 	image_queue = list()
# 	while True:
# 		try:
# 			current_images = set(os.listdir(conf.resized_image_dir))
# 			new_images = processed_images.symmetric_difference(current_images)
# 			new_images = new_images - processed_images
# 			try:
# 				new_images.remove('.DS_Store')
# 			except KeyError:
# 				pass
# 			if new_images:
# 				print new_images
# 				for i in list(new_images): image_queue.append(i)
# 				images_to_show = map(lambda x: app.flaskify(conf.resized_image_dir) + x, image_queue[-5::])
# 				print images_to_show
# 				socketio.emit('update displayed images',
# 					 {'images':images_to_show},
# 					  namespace = '/test')
# 				processed_images = processed_images.union(new_images)
# 			time.sleep(1)
# 		except KeyboardInterrupt:
# 			raise resized_image_dir


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
	# app.run(debug = True)
	socketio.run(app, port = 8080)
	#http_server = HTTPServer(WSGIContainer(app))
	#http_server.listen(5000)
	#IOLoop.instance().start()
