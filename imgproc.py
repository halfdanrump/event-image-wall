"""
Script to be run on the device where the original images are stored
"""
import os
import time
from datetime import datetime
from multiprocessing import Process
from app import conf
def image_processing_daemon():
	# Background thread that monitors 
	start_time = datetime.now()
	processed_images = set()
	while True:
		try:
			current_images = set(os.listdir(conf.original_image_dir))
			new_images = processed_images.symmetric_difference(current_images)
			new_images = new_images - processed_images
			try:
				new_images.remove('.DS_Store')
			except KeyError:
				pass
			if new_images:
				print 'Uptime %s - %s'%(str(datetime.now() - start_time), new_images)
				process_images(new_images)
				processed_images = processed_images.union(new_images)
			time.sleep(1)
		except KeyboardInterrupt:
			raise resized_image_dir

from PIL import Image
import httplib
def process_images(images_to_process):
	for image_name in images_to_process:
		current_image_dir = conf.original_image_dir
		print 'Processing image: %s'%(current_image_dir + image_name)
		new_image_path = resize_image(current_image_dir, image_name)
		upload_image(new_image_path)			
		


from random import gauss
def resize_image(current_image_dir, image_name):
	
	image = Image.open(current_image_dir + image_name)
	w,h = conf.original_image_size
	scale_factor = gauss(conf.scale_mean, conf.scale_std)
	resized_image_size = (int(h * scale_factor), int(w*scale_factor))
	# print resized_image_size
	image = image.resize(resized_image_size)
	resized_image_path = conf.resized_image_dir + 'resized_' + image_name
	image.save(resized_image_path)	
	return resized_image_path

import urllib2
def upload_image(image_path):
	url = "http://107.170.251.142/upload"
	header = {'Content-Type': 'image/jpeg'}
	with open(image_path) as f:
		image = f.read()
	try:
		request = urllib2.Request(url, image, header)
		response = urllib2.urlopen(request)
	except Exception, e:
		print e


# from app.conf import remote_host, remote_port
# def upload_image(image_path):
# 	try:
# 		host = '%s:%s'%(remote_host, remote_port)
# 		print host
# 		h = httplib.HTTPConnection(host = host)
# 	except IOError:
# 			print 'Could not open connection to server! Make sure it is running...'

# 	h.set_debuglevel(conf.http_debug_level)
# 	with open(image_path) as f:
# 		data = {'image_data':f.read(), 'image_name':image_path}
# 		h.request('post', '/upload', body = repr(data))
# 		response = h.getresponse()
# 		print response.status
# 	# with open(image_path) as f:
		
	
if __name__ == "__main__":
	Process(target = image_processing_daemon).start()



