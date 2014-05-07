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

def image_processing_daemon():
	print 'Scanning folder %s for new pictures'%args.image_folder
	start_time = datetime.now()
	processed_images = set()
	while True:
		try:
			new_images = set(os.listdir(args.image_folder))
			try:
				new_images.remove('.DS_Store')
			except KeyError:
				pass
			if new_images:
				print 'Uptime %s - %s'%(str(datetime.now() - start_time), new_images)
				process_images(new_images)
				processed_images = processed_images.union(new_images)
		except KeyboardInterrupt:
			raise
		time.sleep(1)


def process_images(images_to_process):
	for image_name in images_to_process:
		current_image_dir = args.image_folder
		new_image_path = current_image_dir + image_name
		print 'Processing image: %s'%(current_image_dir + image_name)
		# IMAGE PIPELINE START
		new_image_paths = resize_image(current_image_dir, image_name)
		# IMAGE PIPELINE END
		for new_image_path in new_image_paths:
			upload_image(new_image_path)
		move_image(image_name)

# def monochrome(image_name):
# 	image = Image.open(image_name)
# 	image = image.convert('L')
# 	image = image.filter(ImageFilter.ModeFilter(size = 10))
# 	image = ImageEnhance.Contrast(image).enhance(2)

def apply_random_processing(image_name, save_folder):
	image = Image.open(image_name)
	
	def preset_1(image):
		return ImageEnhance.Contrast(image.convert('L')).enhance(2).filter(ImageFilter.ModeFilter(size = 10)).filter(ImageFilter.CONTOUR())

	def preset_2(image):
		return image.filter(ImageFilter.MedianFilter(size = 10))
	
	processed_image = eval('preset_%s'%random.sample([1,2],1)[0])(image)
	processed_images.save(save_folder + uuid.uuid4().hex)


def move_image(image_name):
	print "Moving %s to %s"%(args.image_folder + image_name, args.untouched_folder + image_name)
	shutil.move(args.image_folder + image_name, args.untouched_folder + image_name)



def resize_image(current_image_dir, image_name):
	image = Image.open(current_image_dir + image_name)
	dim = list(image.size)
	resized_image_paths = list()
	for scaling in args.resize_ratios:
		try:
			new_dim = tuple(map(lambda x: int(x / float(scaling)), dim))
			print 'Resizing %s %s to %s'%(image_name, dim, new_dim)
			image = image.resize(new_dim, Image.ANTIALIAS)
			new_image_name = 'resized_%s'%scaling + image_name
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
	
	if args.behavior == 'queue':
		args.resize_ratios = [8]
	elif args.behavior == 'random':
		args.resize_ratios = [4, 8, 16, 32, 48]

	if args.production:
		from conf import Production
		config = Production()
	else:
		from conf import Development
		config = Development()
		print config.HOST
	image_processing_daemon()

