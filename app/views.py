from app import app
from flask import render_template

@app.route('/')
@app.route('/')
def index():
	return render_template('wall.html')

@app.route('/upload', methods = ['GET'])
def upload():
	return render_template('wall.html')
