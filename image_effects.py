from PIL import Image, ImageEnhance, ImageFilter, ImageDraw

def resize(image, scaling = 4):
	dim = list(image.size)
	new_dim = tuple(map(lambda x: int(x / float(scaling)), dim))
	return image.resize(new_dim, Image.ANTIALIAS)

def funky_angel(image, l = 100, u = 200):
	return Image.eval(image, lambda x: x if x > l and x < u else 256)

def sketch(image):
	return ImageEnhance.Contrast(image.convert('L')).enhance(2).filter(ImageFilter.ModeFilter(size = 20)).filter(ImageFilter.CONTOUR())

def mode(image, size = 10):
	return image.filter(ImageFilter.ModeFilter(size))

def monochrome(image, threshold = 150):
	return image.convert('L').point(lambda p: p > threshold and 256)

def t(image):
	return Image.eval(image, lambda x: x if x > 100 and x < 200 else 256)

def crop(image, radius = 1000):
	w, h = image.size
	mw = w / 2
	mh = h / 2
	box = (mw - radius, mh - radius, mw + radius, mh + radius)
	return image.crop(box)


def get_mask(image, fill = 255):
	image = crop(image)
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
	cropped = crop(image)
	circle = get_circle(cropped)
	cropped.paste(circle, mask = circle)
	return cropped

def pipeline(image, *args):
	for arg in args:
		if isinstance(arg, list):
			func = arg[0]
			fargs = arg[1::]
		elif callable(arg):
			func = arg
			fargs = list()
		image = func(image, *fargs)
	return image

import struct
def hex2rgb(hexstr):
	return struct.pack('BBB', hexstr.decode('hex'))

def rgb2hex(rgb):
	return struct.pack('BBB', *rgb).encode('hex')


