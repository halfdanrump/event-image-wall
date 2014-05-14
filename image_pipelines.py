import image_effects as ie
import brewer2mpl
from random import sample

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

def use_brewer_background(image, pipeline_func, **pipeline_kwargs):
	hex_colors = [c.replace('#','') for c in brewer2mpl.get_map('RdYlGn', 'Diverging', 11).hex_colors]
	background_color = sample(hex_colors, 1)[0]
	return pipeline_func(image, background_color, **pipeline_kwargs)

def bloodyface(image, darker_color = '3c5c47', brigther_color = 'b0e4e0'):
	return pipeline(image, ie.crop, [ie.color_filter, darker_color, brigther_color, (120,0,0)], ie.mode, ie.apply_circle_mask)

def sketch(image, background_color = 'FFFFFF', gain = 2, mode_size = 5):
	return pipeline(image, ie.crop, [ie.sketch, gain, mode_size], [ie.colorize, background_color], ie.apply_circle_mask)

def monochrome(image, width, height, hex_color = 'FFFFFF', monochrome_treshold = 100):
	return pipeline(image, ie.crop, [ie.monochrome, monochrome_treshold], [ie.colorize, hex_color], ie.apply_circle_mask, [ie.resize_to_size, width, height])

def funky_angel(image):
	return pipeline(image, ie.crop, [ie.funky_angel, 50, 200], [ie.mode, 55], ie.apply_circle_mask)

def random_scale_and_flip(image, scale_bound_low = 0.01, scale_bound_high = 0.25):
	return pipeline(image, [ie.resize, None, scale_bound_low, scale_bound_high, True], ie.random_flip)

def constant_scale(image, scale = 0.25):
	return pipeline(image, ie.crop, ie.apply_circle_mask, [ie.resize, scale, None, None, False])

