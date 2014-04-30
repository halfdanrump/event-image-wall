from app import app, socketio, conf
from threading import Thread

import os
from random import sample, gauss
import time

#from tornado.wsgi import WSGIContainer
#from tornado.httpserver import HTTPServer
#from tornado.ioloop import IOLoop


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
	socketio.run(app, port = 8080)
	#http_server = HTTPServer(WSGIContainer(app))
	#http_server.listen(5000)
	#IOLoop.instance().start()
