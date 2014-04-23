from app import app

@app.route('/')
@app.route('/')
def index():
	return 'welcome to event image map'

@app.route('/upload', methods = ['GET'])
def upload():
	return 'upload page'
