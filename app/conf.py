import os

class BasicConfig():
	
	REDIS_WALL_Q = 'showing'
	REDIS_ALL_Q = 'all'	
	DEBUG = True
	PROPAGATE_EXCEPTIONS = True

	N_WALLPICS = 5
	WALL_BEHAVIOR = 'QUEUE'
	ORIGINAL_IMAGE_DIR = 'app/static/images/original/'
	RESIZED_IMAGE_DIR = 'app/static/images/resized/'

	def makedir(self, dir):
		try:
			os.makedirs(dir)
		except OSError:
			pass

	def __init__(self):
		self.makedir(ORIGINAL_IMAGE_DIR)


class Production(BasicConfig):
	HOST = 'http://107.170.251.142'
	PORT = '80'

class Development(BasicConfig):
	HOST = 'http://127.0.0.1'
	PORT = '8080'

remote_host = 'http://107.170.251.142'
remote_port = '80'

original_image_size = (2784, 1848)

target_size = (320, 200)

