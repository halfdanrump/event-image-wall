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

scale_mean = 0.3
scale_std = 0.1

http_debug_level = 0

number_of_pictures_on_wall = 3
