"""
Script to be run on the device where the original images are stored

Example: python imgproc.py -i app/static/images/original/ -t tmp/ -r 8 -r 4
"""
import os
import time
from datetime import datetime
from multiprocessing import Process

import argparse

parser = argparse.ArgumentParser(description = 'Run to upload images to server as they are placed in the image folder')
parser.add_argument('-i', '--image-folder', help = 'Specify image folder', required = True)
parser.add_argument('-t', '--temp-folder', help = 'Specify image folder', required = True)
parser.add_argument('-r', '--resize-ratios', help = 'Specify integers that the image dimensions will be divided by', type = int, action = 'append')
args = parser.parse_args()

if not hasattr(args, 'resize_ratios'):
	args.resize_ratios = [4, 8]

print args

def image_processing_daemon():
	start_time = datetime.now()
	processed_images = set()
	while True:
		try:
			current_images = set(os.listdir(args.image_folder))
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
			raise

from PIL import Image
import httplib
def process_images(images_to_process):
	for image_name in images_to_process:
		current_image_dir = args.image_folder
		new_image_path = current_image_dir + image_name
		print 'Processing image: %s'%(current_image_dir + image_name)
		new_image_paths = resize_image(current_image_dir, image_name)
		for new_image_path in new_image_paths:
			upload_image(new_image_path)			

from random import gauss, sample
def resize_image(current_image_dir, image_name):
	image = Image.open(current_image_dir + image_name)
	dim = list(image.size)
	resized_image_paths = list()
	for scaling in args.resize_ratios:
		try:
			new_dim = tuple(map(lambda x: int(x / float(scaling)), dim))
			print 'Resizing %s %s to %s'%(image_name, dim, new_dim)
			image = image.resize(new_dim, Image.ANTIALIAS)
			resized_image_path = args.temp_folder + 'resized_%s'%scaling + image_name
			image.save(resized_image_path)
			resized_image_paths.append(resized_image_path)
		except Exception, e:
			print e
	
	return resized_image_paths



import urllib2
def upload_image(image_path):
	url = '%s:%s/upload'%(app.config['HOST'], app.config['PORT'])
	print url
	header = {'Content-Type': 'image/jpeg'}
	with open(image_path) as f:
		image = f.read()
	try:
		request = urllib2.Request(url, image, header)
		response = urllib2.urlopen(request)
	except Exception, e:
		print e
		
	
if __name__ == "__main__":
	Process(target = image_processing_daemon).start()



