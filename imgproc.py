"""
Script to be run on the device where the original images are stored

Example: $ python imgproc.py -i app/static/images/original/ -t tmp/ -u untouched/ -b queue
"""
import os
from os.path import join as joinpath
import time
from datetime import datetime
from multiprocessing import Process
import random
import uuid

import argparse
from PIL import Image, ImageFilter, ImageEnhance
import shutil
from random import gauss, sample
import urllib2
from glob import glob
import image_effects as ie
import image_pipelines as ip

import logging, logging.handlers
logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('IMGPROC')
logger.setLevel('DEBUG')
import brewer2mpl

# handler = logging.handlers.RotatingFileHandler('imgproc.log', maxBytes = 10**6)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)

class Config(object):
	GRID_NVERSION = 1
	RANDOM_NVERSIONS = 10
	GRID_IMAGE_SIZE = (350, 350)
	# GRID_IMAGE_SIZE = (1200,1200)
	# GRID_IMAGE_SIZE = (200, 200)
	QUEUE_IMAGE_SIZE = (350, 350)
	COLORMAP = brewer2mpl.get_map('RdYlGn', 'Diverging', 11)

	RANDOM_SCALING_ALPHA = 2
	RANDOM_SCALING_GAMMA = 5
	RANDON_SCALING_MAX = 0.5

	def random_color(self):
		hex_colors = [c.replace('#','') for c in self.COLORMAP.hex_colors]
		color = sample(hex_colors, 1)[0]
		return color


def move_image(image_name):
	source_name = joinpath(args.image_folder, image_name)
	target_name = joinpath(args.untouched_folder, image_name)
	logger.info("Moving %s to %s"%(source_name, target_name))
	shutil.move(source_name, target_name)


def save_image(image):
	new_image_path = joinpath(args.temp_folder, uuid.uuid4().hex) + '.jpg'
	logger.debug('Saving image to %s'%new_image_path)
	image.save(new_image_path, quality = 100)
	return new_image_path
	


def image_processing_daemon():
	logger.info('####################################################')
	logger.info('Scanning folder %s for new pictures'%args.image_folder)
	while True:
		try:
			new_images = map(lambda ftype: glob(joinpath(image_dir, ftype)), ['*.jpg', '*.JPG'])
			new_images = set([f.split('/')[-1] for sublist in new_images for f in sublist])
			if new_images:
				process_images(new_images)
		except KeyboardInterrupt:
			raise
		time.sleep(1)



def process_images(images_to_process):
	for image_name in images_to_process:
		image_source_dir = image_dir
		
		try:
			image = Image.open(image_source_dir + image_name)	
		
			if args.processing_type == 'queue':
				queue_processing(image)
				grid_processing(image)
			elif args.processing_type == 'random':
				random_processing(image)
			elif args.processing_type == 'grid':
				grid_processing(image)
			elif args.processing_type == 'all':
				queue_processing(image)
				grid_processing(image)
				random_processing(image)
		
			move_image(image_name)
		
		except IOError, e:
			logger.exception('EXCEPTION!!!!: %s'%e)




def queue_processing(image):
	width, height = config.QUEUE_IMAGE_SIZE	
	processed_image = ip.monochrome(image, config.random_color(), 110, white_background = False)
	processed_image = ie.resize_to_size(processed_image, width, height)
	image_path = save_image(processed_image)
	upload_image(image_path, URL_BASE + '/upload_queue_image')
	# image = ip.pipeline(image, ie.crop, ie.apply_circle_mask, [ie.resize_to_size, width, height])
	# image_path = save_image(image)
	# url = URL_BASE + '/upload_queue_image'
	# upload_image(image_path, url)


def grid_processing(image):
	width, height = config.GRID_IMAGE_SIZE
	for i in range(config.GRID_NVERSION):	
		if args.grid_processing == 'sketch':
			# gain = abs(random.gauss(2, 1))
			# mode_size = sample(range(3, 33, 2), 1)[0]
			gain = 2
			mode_size = 11
			processed_image = ip.sketch(image, gain = gain, mode_size = mode_size)	
			processed_image = ie.resize_to_size(processed_image, width, height)
			image_path = save_image(processed_image)
			upload_image(image_path, URL_BASE + '/upload_grid_image')
		elif args.grid_processing == 'monochrome':
			processed_image_white = ip.monochrome(image, config.random_color(), 110)
			processed_image_white = ie.resize_to_size(processed_image_white, width, height)
			image_path_white = save_image(processed_image_white)
			upload_image(image_path_white, URL_BASE + '/upload_grid_image_white')

			processed_image_black = ip.monochrome(image, config.random_color(), 110, white_background = False)
			processed_image_black = ie.resize_to_size(processed_image_black, width, height)
			image_path_black = save_image(processed_image_black)
			upload_image(image_path_black, URL_BASE + '/upload_grid_image_black')
			


def random_processing(image):
	for i in range(config.RANDOM_NVERSIONS):
		r = random.randint(0, 2)
		print r
		if r == 0:
			processed_image = ip.monochrome(image, config.random_color(), 100)
			# processed_image = ip.monochrome(image, config.random_color(), int(random.gauss(100, 30)))
		if r == 1:
			processed_image = ip.bloodyface(image)
		if r == 2:
			gain = abs(random.gauss(2, 1))
			mode_size = sample(range(3, 33, 2), 1)[0]
			processed_image = ip.sketch(image, gain = gain, mode_size = mode_size)
		processed_image = ie.random_resize(processed_image, config.RANDOM_SCALING_ALPHA, config.RANDOM_SCALING_GAMMA)

		image_path = save_image(processed_image)
		url = URL_BASE + '/upload_random_image'
		upload_image(image_path, url)			



def upload_image(image_path, url):
	logger.info('Uploading %s to %s'%(image_path, url))
	header = {'Content-Type': 'image/jpeg'}
	with open(image_path) as f:
		image = f.read()
	try:
		request = urllib2.Request(url, image, header)
		response = urllib2.urlopen(request)
	except Exception, e:
		print e
		
	
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = 'Run to upload images to server as they are placed in the image folder')
	parser.add_argument('-ud', '--upload-destination', choices = ('local', 'remote'), required = True)
	parser.add_argument('-i', '--image-folder', help = 'Specify image folder to monitor for new images', required = True)
	parser.add_argument('-u', '--untouched-folder', help = 'Specify where to move untouched images', required = True)
	parser.add_argument('-t', '--temp-folder', help = 'Specify temp folder where processed images are stored', required = True)
	parser.add_argument('-pt', '--processing-type', help = 'Specify how the images should be resized to fit with display style', choices = ('queue', 'random', 'grid', 'all'))
	parser.add_argument('-gp', '--grid-processing', choices = ('monochrome', 'sketch'))
	
	args = parser.parse_args()
	basedir = os.path.abspath(os.path.dirname(__file__))
	image_dir = os.path.join(basedir, args.image_folder)
		
	config = Config()

	if args.upload_destination == 'local':
		URL_BASE = 'http://127.0.0.1:8080'
	elif args.upload_destination == 'remote':
		URL_BASE = 'http://107.170.251.142:80'	

	image_processing_daemon()

