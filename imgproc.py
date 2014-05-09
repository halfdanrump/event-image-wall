"""
Script to be run on the device where the original images are stored

Example: $ python imgproc.py -i app/static/images/original/ -t tmp/ -u untouched/ -b queue
"""
import os
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

def image_processing_daemon():
	print 'Scanning folder %s for new pictures'%args.image_folder
	start_time = datetime.now()
	processed_images = set()
	while True:
		try:
			new_images = map(lambda ftype: glob(os.path.join(image_dir, ftype)), ['*.jpg', '*.JPG'])
			new_images = set([f.split('/')[-1] for sublist in new_images for f in sublist])
			# new_images = set(os.listdir(args.image_folder))
			# try:
			# 	new_images.remove('.DS_Store')
			# except KeyError:
			# 	pass
			if new_images:
				print 'Uptime %s - %s'%(str(datetime.now() - start_time), new_images)
				process_images(new_images)
				processed_images = processed_images.union(new_images)
		except KeyboardInterrupt:
			raise
		time.sleep(1)

def process_images(images_to_process):
	for image_name in images_to_process:
		image_source_dir = image_dir
		new_image_path = image_source_dir + image_name
		print 'Processing image: %s'%(image_source_dir + image_name)
		# IMAGE PIPELINE START
		new_image_paths = resize_image(image_source_dir, image_name)
		# IMAGE PIPELINE END
		for new_image_path in new_image_paths:
			upload_image(new_image_path)
		move_image(image_name)


def move_image(image_name):
	print "Moving %s to %s"%(args.image_folder + image_name, args.untouched_folder + image_name)
	shutil.move(args.image_folder + image_name, args.untouched_folder + image_name)



def resize_image(current_image_dir, image_name):
	image = Image.open(current_image_dir + image_name)
	resized_image_paths = list()
	for scaling in args.resize_ratios:
		try:
			# image = ie.pipeline(image, ie.apply_circle_mask, [ie.resize, scaling], [ie.funky_angel, 0, 60])
			image = ie.pipeline(image, ie.apply_circle_mask, [ie.resize, scaling], [ie.monochrome, 100], [ie.mode, 3])
			# image = ie.pipeline(image, [ie.resize, scaling], ie.apply_circle_mask, [ie.funky_angel, 0, 60])
			new_image_name = uuid.uuid4().hex + image_name
			new_image_path = args.temp_folder + new_image_name
			
			image.save(new_image_path)
			resized_image_paths.append(new_image_path)
		except Exception, e:
			print e
	
	return resized_image_paths



def upload_image(image_path):
	url = '%s:%s/upload'%(config.HOST, config.PORT)
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
	parser = argparse.ArgumentParser(description = 'Run to upload images to server as they are placed in the image folder')
	parser.add_argument('-p', '--production', help = 'Set production environment', action = "store_true")
	parser.add_argument('-i', '--image-folder', help = 'Specify image folder to monitor for new images', required = True)
	parser.add_argument('-u', '--untouched-folder', help = 'Specify where to move untouched images', required = True)
	parser.add_argument('-t', '--temp-folder', help = 'Specify temp folder where processed images are stored', required = True)
	parser.add_argument('-b', '--behavior', help = 'Specify how the images should be resized to fit with display style', choices = ('queue', 'random'))
	
	args = parser.parse_args()

	basedir = os.path.abspath(os.path.dirname(__file__))
	image_dir = os.path.join(basedir, args.image_folder)
	print image_dir
	
	if args.behavior == 'queue':
		args.resize_ratios = [4]
	elif args.behavior == 'random':
		args.resize_ratios = [6,8,16]

	if args.production:
		from conf import Production
		config = Production()
	else:
		from conf import Development
		config = Development()
		print config.HOST
	image_processing_daemon()

