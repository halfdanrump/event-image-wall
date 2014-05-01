class BasicConfig():
	REDIS_WALL_Q = 'showing'
	REDIS_ALL_Q = 'all'	
	DEBUG = True
	PROPAGATE_EXCEPTIONS = True

	N_WALLPICS = 5

class Production(BasicConfig):
	HOST = 'http://107.170.251.142'
	PORT = '80'

class Development(BasicConfig):
	HOST = 'http://127.0.0.1'
	PORT = '8080'

remote_host = 'http://107.170.251.142'
remote_port = '80'

original_image_dir = 'app/static/images/original/'
resized_image_dir = 'app/static/images/resized/'

import os
def makedir(dir):
	try:
		os.makedirs(dir)
	except OSError:
		pass

if os.path.isdir('app/static'):
	makedir(original_image_dir)
	makedir(resized_image_dir)

original_image_size = (2784, 1848)

target_size = (320, 200)

scale_mean = 0.2
scale_std = 0.1

http_debug_level = 0

number_of_pictures_on_wall = 64

