from city import *

class Vertex(object):
	
	def __init__(self, name, city):
		self.name = name
		self.edges = {}
		self.city = city

	def construct_edges(self, routes_list):
		''' connects my vertices with edges based on the routes_list from the json file	'''

		for index in range(0, len(routes_list)):
			# routes_list[index] returns a dictionary. "ports" is the key.
			# I'm storing the value mapped to the key which is a list of two city codes
			ports_list = routes_list[index]["ports"]

			# ports_list[0] is the city you are in and ports_list[1] is the destination
			# I'm adding all the straight flight destinations into my dictionary of
			# adjacent cities, with values as distance between the two cities.
			if ports_list[0] == self.city.code:
				dist = routes_list[index]["distance"]
				self.edges[str(ports_list[1])] = dist
			
			# Each vertex of the graph should be two-way. Meaning if there's a flight
			# from city1 to city2, then there's also a flight from city2 to city1.
			# So here I'm checking to see if this city is a destination from any other
			# cities. If it is, then I add those cities the my dictionary of adjacent cities.
			
			if ports_list[1] == self.city.code:
				dist = routes_list[index]["distance"]
				self.edges[str(ports_list[0])] = dist
	
	def add_route(self, route_dict):
		''' connects two vertices with an edge based on the route_list '''
		dest = route_dict["ports"][1]
		self.edges[dest] = route_dict["distance"]
	
	def edit_name(self, graph):
		old_name = self.name
		new_name = raw_input("Type in the name you want for the city or type in -9 to go back to the start screen\n")
		while (new_name != '-9') and (not new_name.isalpha()):
			print "Sorry, your request could not be understood"
			new_name = raw_input("Type in the name you want for the city or type in -9 to go back to the start screen\n")
		
		#return -1 so I know to discard any changes from all edits
		if new_name == '-9':
			return -1
		
		self.name = new_name
		self.city.name = new_name
		graph.vertex_dict[new_name] = self
		graph.vertex_dict.pop(old_name)
		
		#return 0 so I know this returned correctly
		return 0

	def edit_code(self, graph):
		old_code = self.city.code
		new_code = raw_input("Type in the code you want for the city or type in -9 to to go back to the start screen\n")
		while (new_code.isalpha() == False) and (new_code != '-9'):
			print "Sorry, your request cannot be understood"
			new_code = raw_input("Type in the code you want for the city or type in -9 to go back to the start screen\n")
		
		#return -1 so I know to discard any changes from all edits
		if new_code == '-9':
			return -1

		for vertex in graph.vertex_dict:
			curr_vertex = graph.vertex_dict[vertex]
			if old_code in curr_vertex.edges:
				curr_vertex.edges[new_code] = curr_vertex.edges[old_code]
				curr_vertex.edges.pop(old_code)

		return 0

	def edit_routes(self, graph):
		''' Ask if the user wants to add or remove a route. Then add/remove '''
		print "Type in the number corresponding to the option you want"
		input_text = raw_input("1.add route\n2.remove route\n3.go back to the start screen\n")
		while input_text not in ('1','2','3'):
			print "Sorry, your request could not be understood"
			input_text = raw_input("1.add route\n2.remove route\n3.go back to the start screen\n")

		while len(self.edges) == 0 and input_text == '2' and input_text != '1' and input_text != '3':
			print "Sorry, there are no routes for you to remove, you can only add a route or go back to the start screen."
			input_text = raw_input("1.add route\n2.remove route\n3.go back to the start screen\n")

		if input_text == '1':
			dest = raw_input("What do you want the destination to be? Enter the name of a city.\n")
			while dest not in graph.vertex_dict:
				print "Sorry, your input could not be understood."
				dest = raw_input("What do you want the destination to be? Enter the name of a city.\n")
			city = None
			for vertex in graph.vertex_dict:
				if graph.vertex_dict[vertex].name == dest:
					city = graph.vertex_dict[vertex].city
					break
			dist = raw_input("What do you want the distance between the city and the destination to be?\n")
			while dist.isdigit() == False or int(dist) < 0:
				print "Sorry, your input could not be understood."
				dist = raw_input("What do you want the distance between the city and the destination to be?\n")

			dict_info = {"ports":[self.city.code, city.code], "distance":int(dist)}
			self.add_route(dict_info)

		elif input_text == '2':
			print self.edges
			city_code = raw_input("Type in the code of the city that you want removed as a route\n")
			while city_code not in self.edges:
				print "Sorry, your request could not be understood."
				city_code = raw_input("Type in the code of the city that you want removed as a route\n")
			self.edges.pop(city_code)
		
		#return -1 so I know to discard any changes from all edits
		elif input_text == '3':
			return -1

		return 0
			
	def edit_country(self):
		''' Alters the country for the city '''
		country_name = raw_input("Type in the name of the country that you want the city to be in or type in -9 to go back to the start screen\n")
		
		#country name has to be in letters
		while country_name != '-9' and country_name.isalpha() == False:
			print "Sorry, your request cannot be understood"
			country_name = raw_input("Type in the name of the country that you want the city to be in\n")
		
		#return -1 so I know to discard any changes from all edits
		if country_name == '-9':
			return -1

		self.city.country = country_name
		
		return 0

	def edit_continent(self):
		'''Alters the continent for the city '''
		continent_name = raw_input("Type in the name of the continent that you want the city to be in or type in -9 to go back to the start screen\n")
		
		#continent had to be a word, and also replace spaces with nothing because space is not a letter
		while continent_name != '-9' and continent_name.replace(' ','').isalpha() == False:
			print "Sorry, your request cannot be understood"
			continent_name = raw_input("Type in the name of the continent that you want the city to be in\n")

		#return -1 so I know to discard any changes from all edits
		if continent_name == '-9':
			return -1

		self.city.continent = continent_name

	def edit_population(self):
		'''Alters the population for the city '''
		pop = raw_input("Type in the number of people you want in the city or type in -9 to go back to the start screen\n")
		
		#population cannot be negative
		while pop.isdigit() == False or (int(pop) < 0 and int(pop) != '-9'):
			print "Sorry, your request cannot be understood"
			pop = raw_input("Type in the number of people you want in the city or type in -9 to go back to the start screen\n")

		#return -1 so I know to discard any changes from all edits
		if pop == '-9':
			return -1

		self.city.population = int(pop)
		
		return 0

	def edit_timezone(self):
		'''Alters the timezone for the city '''
		timezone = raw_input("Type in the timezone number in gmt that you want the city to be in e.g. -6 or 5 or type in -9 to go back to the start screen\n")
		
		#i needed to replace '-' with nothing, because '-' does not count as a digit
		while not timezone.replace('-','').isdigit():
			print "Sorry, your request cannot be understood"
			timezone = raw_input("Type in the timezone number in gmt that you want the city to be in or type in -9 to go back to the start screen\n")

		#return -1 so I know to discard any changes from all edits
		if timezone == '-9':
			return -1

		self.city.timezone = int(timezone)
	
		return 0

	def edit_coordinates(self):
		'''Alters the coordinates for the city'''
		new_coords = {}
		dir1 = ""
		dir2 = ""
		print "Type in either North or South exactly as shown to specify if the city is in the North or South",
		dir1 = raw_input("or type in -9 to go back to the start screen\n")
		while dir1 != "North" and dir1 != "South" and dir1 != '-9':
			print "Sorry, your request cannot be understood"
			dir1 = raw_input("Type in either North or South exactly as shown to specify if the city is in the North or South or type in -9\n")

		#return -1 so I know to discard any changes from all edits
		if dir1 == '-9':
			return -1

		num1 = raw_input("Type in the number coordinate for your specified direction earlier or type in -9 to go back to the start screen\n")
		
		#coordinates have to be greater than 0
		while num1.isdigit() == False or (num1.isdigit() and (int(num1) < 0 and num1 != '-9')):
			print "Sorry, your request cannot be understood"
			num1 = raw_input("Type in the number coordinate for your specified direction earlier or type in -9 to go back to the start screen\n")

		print "Type in either East or West exactly as shown to specify if the city is in the East or West",
		dir2 = raw_input("or type in -9 to go back to the start screen\n")
		while dir2 != "East" and dir2 != "West" and dir2 != '-9':
			print "Sorry, your request cannot be understood"
			dir2 = raw_input("Type in either East or West exactly as shown to specify if the city is in the East or West or type in -9\n")

		if dir2 == '-9':
			return -1

		num2 = raw_input("Type in the number coordinate for your specified direction earlier or type in -9 to go back to the start screen\n")
		while num2.isdigit() == False or (num2.isdigit() and (int(num2) < 0 and num2 != '-9')):
			print "Sorry, your request cannot be understood"
			num2 = raw_input("Type in the number coordinate for your specfied direction earlier or type in -9 to go back to the start screen\n")

		dir1 = dir1[0]
		dir2= dir2[0]

		new_coords = {dir1: num1, dir2: num2}
		self.city.coordinates = new_coords

		return 0

	def edit_region(self):
		'''Alters the region for the city '''
		region = raw_input("Type in the region that you want the city to be in or type in -9 to go back to the start screen\n")
		#regions can only be from 1-4
		while region.isdigit() == False or (region.isdigit() and (int(region) < 0 or int(region) > 4)):
			print "Sorry, your request cannot be understood"
			region = raw_input("Type in the region that you want the city to be in or type in -9 to go back to the start screen\n")

		#return -1 so I know to discard any changes from all edits
		if region == '-9':
			return -1

		self.city.region = region

		return 0
