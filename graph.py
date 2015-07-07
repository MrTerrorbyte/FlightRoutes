from city import *
from vertex import *

class Graph(object):


	def find_city_name(self, code):
		'''Given the city code, find the city name '''
		for vertex_name in self.vertex_dict:
			if self.vertex_dict[vertex_name].city.code == code:
				return vertex_name
		
		return -1	

	def add_vertex(self,vertex):
		'''
		Adds the given vertex into the vertex dictionary. The dictionary maps the
		vertex name (string) to a vertex object.
		'''
		self.vertex_dict[vertex.name] = vertex
	

	def remove_vertex(self, vertex):
		'''
		Removes the given vertex from the vertex dictionary. Gets rid of edges that
		are connected to this vertex
		'''
		city_code = vertex.city.code
		for key in self.vertex_dict:
			curr_vertex = self.vertex_dict[key]
			if city_code in curr_vertex.edges:
				curr_vertex.edges.pop(city_code, None)
		self.vertex_dict.pop(vertex.name)

	def remove_route(self, route):
		'''
		Removes the given one-way route. Route is a pair. First index is source.
		Second index is desination.
		'''
		source = route[0]
		dest = route[1]
		vertex = self.vertex_dict[source]
		dest_code = ""
		
		for city_name in self.vertex_dict:
			if self.vertex_dict[city_name].name == dest:
				dest_code = self.vertex_dict[city_name].city.code
				break

		vertex.edges.pop(dest_code, None)

	def __init__(self):
		'''	constructor for each graph object. User must pass in a list of city dictionaries '''
		self.vertex_dict = {}
	
	def construct_json_graph(self, cities_list, routes_list):
		'''
		reads the cities and routes part of the json file, and construct a graph based on their data
		'''
		for index in range(0, len(cities_list)):
			dict_in_list = cities_list[index]
			city_name = dict_in_list["name"]
			city = City(cities_list[index])
			vertex = Vertex(city_name, city)
			self.vertex_dict[vertex.name] = vertex

		for name in self.vertex_dict:
			self.vertex_dict[name].construct_edges(routes_list)
		
		return self
	

	def get_longest_flight(self):
		'''
		Iterates over every city object's routes to determine the longest route. This is saved
		in the form of a triple (origin, destination, distance). This triple is then printed.
		'''
		longest_dist = 0
		longest_flight = None, None, None
		
		for vertex in self.vertex_dict:
			curr_vertex = self.vertex_dict[vertex]
			curr_city = curr_vertex.city
			# edgeCode is the code for the adjacent city. edges a dictionary
			# that maps a destination city's code with the distance.
			for edgeCode in curr_vertex.edges:
				# if a new longest route has been found, update the longest_dist
				# and set self.longest_flight to the new corresponding triple
				if curr_vertex.edges[edgeCode] > longest_dist:
					longest_dist = curr_vertex.edges[edgeCode]
					longest_flight = curr_city.code, edgeCode, longest_dist
		return longest_flight

	def get_shortest_flight(self):
		'''
		Iterates over every city object's routes to determine the shortest route. This is saved
		in the form of a triple (origin, destination, distance). The triple is then printed.
		This is basically the opposite of the get_longest_flight() function.
		'''
		shortest_dist = 100000000
		shortest_flight = None, None, None
		for vertex in self.vertex_dict:
			curr_vertex = self.vertex_dict[vertex]
			curr_city = curr_vertex.city
			for edgeCode in curr_vertex.edges:
				# if a new shortest route has been found, update the shortest_dist
				# and set self.shortest_flight to the new corresponding triple
				if curr_vertex.edges[edgeCode] < shortest_dist:
					shortest_dist = curr_vertex.edges[edgeCode]
					shortest_flight = curr_city.code, edgeCode, shortest_dist
		return shortest_flight
	

	def get_continents(self):
		'''
		I create a dictionary with a key for every continent that's covered in the airline.
		Each key is mapped to a list. This list contains every city in that continent key.
		At the end, I print each continent with its cities followed by a new line.	
		'''
		continents_dict = {}
		for vertex in self.vertex_dict:
			curr_city = self.vertex_dict[vertex].city
			# if the dictionary doesn't contain that continent yet, add it.
			# if the dictionary all ready has the continent, then append
			# the city name to the continent's list.
			if curr_city.continent not in continents_dict:
				continents_dict[curr_city.continent] = []
				continents_dict[curr_city.continent].append(curr_city.name)
			else:
				continents_dict[curr_city.continent].append(curr_city.name)
		
		return continents_dict
		

	def get_biggest_city(self):
		'''
		First finds the city with the largest population. 
		Then returns the city name with its population as a string.
		'''
		largest_pop = 0
		largest_city = None
		for vertex in self.vertex_dict:
			curr_vertex = self.vertex_dict[vertex]
			curr_city = curr_vertex.city
			if curr_city.population > largest_pop:
				largest_pop = curr_city.population
				largest_city = curr_city
		return largest_city.name+': ',largest_pop


	def get_smallest_city(self):
		'''
		First finds the city with the smallest population. 
		Then returns the city name with its population as a string.	
		'''
		smallest_pop = float('inf')
		smallest_city = None
		for vertex in self.vertex_dict:
			curr_vertex = self.vertex_dict[vertex]
			curr_city = curr_vertex.city
			if curr_city.population < smallest_pop:
				smallest_pop = curr_city.population
				smallest_city = curr_city
		return smallest_city.name+': ',smallest_pop
		

	def get_avg_size(self):
		'''
		First stores the number of cities and then sum up every city's population. 
		Returns the average as an integer.
		'''
		num_cities = len(self.vertex_dict)
		total_pop = 0
		for vertex in self.vertex_dict:
			curr_vertex = self.vertex_dict[vertex]
			curr_city = curr_vertex.city
			total_pop += curr_city.population
		return total_pop/num_cities


	def get_avg_distance(self):
		'''
		First stores the number of cities and then sum up every edge (distance) between every city.
		Then returns the average as an integer.
		'''
		num_edges = 0
		total_dist = 0
		for vertex in self.vertex_dict:
			curr_vertex = self.vertex_dict[vertex]
			for edgeCode in curr_vertex.edges:
				total_dist += curr_vertex.edges[edgeCode]
				num_edges += 1.0
		return total_dist/num_edges


	def get_hub_cities(self):
		'''
		I'm assuming a city is considered a hub if it has a straight flight to 5 or more cities.
		I create a list of these cities.
		'''
		hub_list = []
		for vertex in self.vertex_dict:
			curr_vertex = self.vertex_dict[vertex]

			# each edge represents a route
			if len(curr_vertex.edges) > 5:
				hub_list.append(curr_vertex.city.name)
		return hub_list


	def get_all_cities(self):
		'''
		Stores every city's name into a list and return the list.
		'''
		cities_list = []
		for vertex in self.vertex_dict:
			cities_list.append(self.vertex_dict[vertex].city.name)
		return cities_list


	def print_stats(self):
		'''
		Prints the statistical info about the graph
		'''
		print "CSAir\'s longest flight:", self.get_longest_flight()
		print "CSAir\'s shortest flight:", self.get_shortest_flight(),"\n"
		
		print "list of continents and their cities that we have flights to"
		continents_dict = self.get_continents()    
		for continent in continents_dict:
			print continent,':',continents_dict[continent],'\n'
		
		print "biggest city:",self.get_biggest_city(),"people"
		print "smallest city:",self.get_smallest_city(),"people"
		print "Average size of cities:",self.get_avg_size(),"people"
		print "Average distance:",self.get_avg_distance()
		print "Hubs:",self.get_hub_cities()
		print '\n'


	def get_url(self):
		'''
		gets the url for the visual map
		'''
		url ="http://www.gcmap.com/mapui?P="
		for vertex in self.vertex_dict:
			curr_vertex = self.vertex_dict[vertex]
			for edgeCode in curr_vertex.edges:
				url += curr_vertex.city.code+"-"+edgeCode+","
		url = url[0:len(url)-1]
		return url
