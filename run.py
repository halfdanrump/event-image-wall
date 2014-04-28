from app import app, socketio
import app.config as conf
from threading import Thread

import os
from random import sample, gauss
import time


def image_monitor():
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
	Thread(target = image_monitor).start()
	# app.run(debug = True)
	socketio.run(app, host = '127.0.0.1', port = 8080)
