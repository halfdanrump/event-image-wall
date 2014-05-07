import os


class BasicConfig():
	
	REDIS_WALL_Q = 'showing'
	REDIS_ALL_Q = 'all'	
	DEBUG = True
	PROPAGATE_EXCEPTIONS = True

	N_WALLPICS = 5
	WALL_BEHAVIOR = 'QUEUE'
	ORIGINAL_IMAGE_DIR = 'app/static/images/original/'
	
	def makedir(self, dir):
		try:
			os.makedirs(dir)
		except OSError:
			pass

	def __init__(self, behavior, wall_refresh_rate):
		
		if behavior == 'queue':
			self.IMAGE_UPLOAD_DIR = 'app/static/images/uploaded/queue/'
		elif behavior == 'random':
			self.IMAGE_UPLOAD_DIR =  'app/static/images/uploaded/random/'
		
		self.WALL_REFRESH_RATE = wall_refresh_rate

		self.makedir(self.ORIGINAL_IMAGE_DIR)
		self.makedir(self.IMAGE_UPLOAD_DIR)

	def __getitem__(self, item):
		return getattr(self, item)


class Production(BasicConfig):
	HOST = 'http://107.170.251.142'
	PORT = '80'
	def __init__(self, **kwargs):
		BasicConfig.__init__(self, **kwargs)

class Development(BasicConfig):
	HOST = 'http://127.0.0.1'
	PORT = '8080'
	def __init__(self, **kwargs):
		BasicConfig.__init__(self, **kwargs)