remote_host = '107.170.251.142'
remote_port = '80'

original_image_dir = 'app/static/images/original/'
resized_image_dir = 'app/static/images/resized/'

import os
def makedir(dir):
	try:
		os.makedirs(dir)
	except OSError:
		pass

if __name__ == "app.config":
	makedir(original_image_dir)
	makedir(resized_image_dir)

original_image_size = (2784, 1848)
scale_mean = 0.1
scale_std = 0.03

http_debug_level = 0

number_of_pictures_on_wall = 3