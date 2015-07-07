
class City(object):

	def init_coords(self, coords_info):
		'''
		This inits the coordinates for the city object taken from the json file.
		I decided to do it this way because json is written in unicode, and so
		when I print the coords, i get the "u" in front of my keys.
		Here I use str(key) to turn them to ascii encoding to get rid of the "u."
		'''	
		for key in coords_info:
			self.coordinates[str(key)] = coords_info[key]
	
	def __init__(self, dict_info):
		'''
		constructor for each city object. User must pass in a dictionary from the
		"metros" list which contains the information about a given city. 
		User must also pass in a list of all the routes. This list
		is a list of dictionaries with keys called "ports" and "distance."
		'''
		self.code = str(dict_info["code"])
		self.name = str(dict_info["name"])
		self.country = str(dict_info["country"])
		self.continent = str(dict_info["continent"])
		self.timezone = dict_info["timezone"]
		self.coordinates = {}
		self.init_coords(dict_info["coordinates"])
		self.population = dict_info["population"]
		self.region = dict_info["region"]

	def print_city_info(self):
		print "name: "+self.name
		print "code: "+self.code
		print "country: "+self.country
		print "continent: "+self.continent
		print "timezone: ",self.timezone
		print "coordinates:",self.coordinates
		print "population:",self.population
		print "region:",self.region

