from PIL import Image, ImageEnhance, ImageFilter, ImageDraw
from imgproc import logger
import random
import numpy as np
import math

def resize(image, constant_scale_factor = 0.25, scale_bound_low = 0.1, scale_bound_high = 0.5, random_scaling = False):
	if random_scaling: 
		scaling = math.log(1 + scale_bound_low + random.random() * (scale_bound_high - scale_bound_low))
	else: 
		scaling = constant_scale_factor
	dim = list(image.size)
	new_dim = tuple(map(lambda x: int(x * float(scaling)), dim))
	logger.debug('Resizing image by factor %s from %s to %s'%(scaling, dim, new_dim))
	return image.resize(new_dim, Image.ANTIALIAS)

def funky_angel(image, l = 100, u = 200):
	return Image.eval(image, lambda x: x if x > l and x < u else random.randint(0, 256))

def sketch(image, gain = 2, mode_size = 5):
	return ImageEnhance.Contrast(image.convert('L')).enhance(gain).filter(ImageFilter.ModeFilter(mode_size)).filter(ImageFilter.CONTOUR())

def mode(image, size = 10):
	return image.filter(ImageFilter.ModeFilter(size))

def monochrome(image, threshold = 150):
	return image.convert('L').point(lambda p: p > threshold and 256)

def random_flip(image):
	if random.random() > 1: image = image.transpose(Image.FLIP_LEFT_RIGHT)
	return image

def t(image):
	return Image.eval(image, lambda x: x if x > 100 and x < 200 else 256)

def crop(image):
	w, h = image.size
	radius = int(h * 0.9 / 2)
	mw = w / 2
	mh = h / 2
	logger.debug('Cropping image from %s to %s'%(image.size, (radius * 2, radius * 2)))
	box = (mw - radius, mh - radius, mw + radius, mh + radius)
	return image.crop(box)


def get_mask(image, fill = 255):
	bigsize = (image.size[0] * 1, image.size[1] * 1)
	mask = Image.new('RGBA', bigsize, 0)
	draw = ImageDraw.Draw(mask) 
	draw.ellipse((0, 0) + bigsize, fill=fill)
	return mask

def get_circle(image):
	mask = Image.new('L', image.size, 255)
	draw = ImageDraw.Draw(mask) 
	draw.ellipse((0, 0) + image.size, fill=0)
	return mask

def apply_circle_mask(image):
	circle = get_circle(image)
	image.paste(circle, mask = circle)
	return image

def colorize(image, hex_color):
	rgb_tuple = hex2rgb(hex_color)
	image = image.convert('RGB')
	data = np.array(image)   # "data" is a height x width x 4 numpy array
	red, green, blue = data.T # Temporarily unpack the bands for readability

	# Replace white with red... (leaves alpha values alone...)
	white_areas = (red == 255) & (green == 255) & (blue == 255) 

	data[np.transpose(white_areas)] = rgb_tuple
	return Image.fromarray(data)
	

def color_filter(image, color_lower = '3c5c47', color_upper = 'b0e4e0', color_fill = None):
	red_l, green_l, blue_l = hex2rgb(color_lower)
	red_u, green_u, blue_u = hex2rgb(color_upper)
	if not color_fill: color_fill = ((red_u + red_l) / 2, (green_u + green_l) / 2, (blue_u + blue_l) / 2)
	image = image.convert('RGB')
	data = np.array(image)   # "data" is a height x width x 4 numpy array
	red, green, blue = data.T # Temporarily unpack the bands for readability
	mask = (red_l < red) & (red < red_u) & (green_l < green) & (green < green_u) & (blue_l < blue) & (blue < blue_u)
	data[np.transpose(mask)] = color_fill
	return Image.fromarray(data)



import struct
def hex2rgb(hexstr):
	return struct.unpack('BBB', hexstr.decode('hex'))

def rgb2hex(rgb):
	return struct.pack('BBB', *rgb).encode('hex')


