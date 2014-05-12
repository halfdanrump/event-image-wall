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
logger.setLevel('INFO')
# handler = logging.handlers.RotatingFileHandler('imgproc.log', maxBytes = 10**6)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)

def image_processing_daemon():
	logger.info('####################################################')
	logger.info('Scanning folder %s for new pictures'%args.image_folder)
	start_time = datetime.now()
	processed_images = set()
	while True:
		try:
			new_images = map(lambda ftype: glob(joinpath(image_dir, ftype)), ['*.jpg', '*.JPG'])
			new_images = set([f.split('/')[-1] for sublist in new_images for f in sublist])
			if new_images:
				process_images(new_images)
				processed_images = processed_images.union(new_images)
		except KeyboardInterrupt:
			raise
		time.sleep(1)

def process_images(images_to_process):
	for image_name in images_to_process:
		image_source_dir = image_dir
		new_image_path = image_source_dir + image_name
		logger.info('Processing image: %s'%image_name)
		new_image_paths = resize_image(image_source_dir, image_name)
		move_image(image_name)


def move_image(image_name):
	source_name = joinpath(args.image_folder, image_name)
	target_name = joinpath(args.untouched_folder, image_name)
	logger.info("Moving %s to %s"%(source_name, target_name))
	shutil.move(source_name, target_name)



def resize_image(current_image_dir, image_name):
	image = Image.open(current_image_dir + image_name)
	# preprocessed_image = ie.pipeline(image, ie.crop, ie.apply_circle_mask, [ie.monochrome, 100])
	for scaling in args.resize_ratios:
		try:
			logger.info('Putting %s through processing pipeline'%image_name)

			if args.image_processing == 'monochrome':
				processed_image = ip.use_brewer_background(image, ip.monochrome)
			elif args.image_processing == 'bloodyface':
				processed_image = ip.bloodyface(image)
			elif args.image_processing == 'sketch':
				processed_image = ip.use_brewer_background(image, ip.sketch, gain = 2, mode_size = 11)
			else:
				processed_image = image
			
			if args.behavior == 'random':
				processed_image = ip.random_scale_and_flip(processed_image)
			elif args.behavior == 'queue':
				processed_image = ip.constant_scale(processed_image)
			
	
			new_image_path = joinpath(args.temp_folder, uuid.uuid4().hex + image_name)
			processed_image.save(new_image_path, quality = 100)
			upload_image(new_image_path)
		
		except Exception, e:
			logger.exception(e)



def upload_image(image_path):
	url = '%s:%s/upload'%(config.HOST, config.PORT)
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
	parser.add_argument('-p', '--production', help = 'Set production environment', action = "store_true")
	parser.add_argument('-i', '--image-folder', help = 'Specify image folder to monitor for new images', required = True)
	parser.add_argument('-u', '--untouched-folder', help = 'Specify where to move untouched images', required = True)
	parser.add_argument('-t', '--temp-folder', help = 'Specify temp folder where processed images are stored', required = True)
	parser.add_argument('-b', '--behavior', help = 'Specify how the images should be resized to fit with display style', choices = ('queue', 'random'))
	parser.add_argument('-ip', '--image-processing', help = 'Specify how the images should be resized to fit with display style', choices = ('monochrome', 'bloodyface', 'sketch'))
	
	args = parser.parse_args()

	basedir = os.path.abspath(os.path.dirname(__file__))
	image_dir = os.path.join(basedir, args.image_folder)
	print image_dir
	
	if args.behavior == 'queue':
		args.resize_ratios = [4]
	elif args.behavior == 'random':
		args.resize_ratios = [6,8,16, 23, 4]

	if args.production:
		from conf import Production
		config = Production()
	else:
		from conf import Development
		config = Development()
		print config.HOST
	image_processing_daemon()

