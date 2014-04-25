from app import app, socketio
#app.run(debug = True)
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import app.config as conf
from threading import Thread

import os
from random import sample, gauss
import time


def image_monitor():
	while True:
		time.sleep(abs(gauss(0.5, 0.5)) + 0.01)
		images = set(os.listdir(conf.resized_image_dir))
		images.remove('.DS_Store')
		images = set(map(lambda x: app.flaskify(conf.resized_image_dir) + x, images))
		selected_images = sample(images, min(conf.number_of_pictures_on_wall, len(images)))
		# with app.app_context():
		socketio.emit('update displayed images',
					 {'images':selected_images},
					  namespace = '/test')

if __name__ == "__main__":
	Thread(target = image_monitor).start()
	# app.run(debug = True)
	socketio.run(app, host = '127.0.0.1', port = 5000)
# http_server = HTTPServer(WSGIContainer(app))
# http_server.listen(5000)
# IOLoop.instance().start()
