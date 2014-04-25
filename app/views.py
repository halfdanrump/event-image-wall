from app import app
from flask import render_template, request
import os
import app.config as conf


@app.route('/')
def index():
	print conf.resized_image_dir
	images = set(os.listdir(conf.resized_image_dir))
	images.remove('.DS_Store')
	images = set(map(lambda x: app.flaskify(conf.resized_image_dir) + x, images))
	print images
	return render_template('wall.html', images = images)

@app.route('/new', )
def new_image(images):
	print images

@app.route('/upload', methods = ['POST'])
def upload():
	# save received image to /static/images
	# emit event to client telling it to append images
	print 'IMAGE UPLOAD'
	data = eval(request.data)
	print ''.join(data['image_name'].split('/')[-2::])
	return render_template('wall.html')
