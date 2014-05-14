import os


class BasicConfig():
	
	REDIS_WALL_Q = 'showing'
	REDIS_ALL_Q = 'all'	
	DEBUG = True
	PROPAGATE_EXCEPTIONS = True

	ORIGINAL_IMAGE_DIR = 'app/static/images/original/'
	
	def makedir(self, dir):
		try:
			os.makedirs(dir)
		except OSError:
			pass

	def __init__(self, wall_refresh_rate):
		
		self.QUEUE_DIR = 'app/static/images/uploaded/queue/'
		self.RANDOM_DIR = 'app/static/images/uploaded/random/'
		self.GRID_DIR = 'app/static/images/uploaded/grid/'
		self.makedir(self.QUEUE_DIR)
		self.makedir(self.RANDOM_DIR)
		self.makedir(self.GRID_DIR)


		self.WALL_REFRESH_RATE = wall_refresh_rate

		self.N_RANDOM_WALLPICS = 10
		self.N_QUEUE_WALLPICS = 10
		
		self.N_GRID_ROWS = 4
		self.N_GRID_COLUMNS = 8

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