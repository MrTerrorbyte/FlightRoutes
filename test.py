from graph import *
import unittest
import json
import calculations
from priority import *

class TestGraph(unittest.TestCase):
	
	def setUp(self):
		''' initializes the variables that I will be using for testing '''
		json_file = open("map_data.json")
		json_data = json.load(json_file)
		json_file.close()
		self.graph = Graph()
		self.metros = json_data["metros"]
		self.routes = json_data["routes"]
		self.graph = self.graph.construct_json_graph(self.metros, self.routes)
		self.priority_queue = PriorityQueue()

	def test_add_to_queue(self):
		''' tests to make sure I can add elements into the queue '''
		self.priority_queue.add("Huitown", 1000)
		self.assertTrue("Huitown" in self.priority_queue.queue)
		self.assertEqual(1000, self.priority_queue.queue["Huitown"])
		
	def test_decrease_priority(self):
		''' tests to make sure I can change priority levels for an element in the queue '''
		self.priority_queue.add("Huitown", float('inf'))
		self.priority_queue.decrease_priority("Huitown", 500)
		self.assertEqual(500, self.priority_queue.queue["Huitown"])

	def test_pop_lowest(self):
		''' tests to make sure that it is the lowest priority element that I pop '''
		self.priority_queue.add('1', 1000)
		self.priority_queue.add('2', 2000)
		self.priority_queue.add('3', 3000)
		self.assertEqual('1', self.priority_queue.pop_lowest())

	def test_calculations(self):
		''' using my json file, tests shortest path, cost, distance, and time '''
		json_file = open("test.json")
		json_data = json.load(json_file)
		json_file.close()
		self.graph = Graph()
		self.metros = json_data["metros"]
		self.routes = json_data["routes"]
		self.graph = self.graph.construct_json_graph(self.metros, self.routes)
		self.assertEqual(['cityTwo','cityOne','cityFour'] , calculations.shortest_path(self.graph, 'cityTwo', 'cityFour'))	
		shortest_path = calculations.shortest_path(self.graph, 'cityTwo', 'cityFour')
		self.assertEqual(['cityTwo', 'cityOne', 'cityFour'] , shortest_path)	
		self.assertEqual(8000, calculations.calculate_dist(self.graph, shortest_path))
		self.assertEqual(804.0, calculations.calculate_time(self.graph, shortest_path))
		self.assertEqual(2550.0, calculations.calculate_cost(self.graph, shortest_path))


	def test_add_vertex(self):
		''' tests that when I add a vertex, it's actually there. '''
		dict_info = {"code":"HUI", "name":"Huitown", "country": "US", "continent": "North America", "timezone": -6, "coordinates": {"N":25, "E":25}, "population": 1, "region": 5}
		city = City(dict_info)
		vertex = Vertex("Huitown", city)
		self.graph.add_vertex(vertex)
		self.assertTrue("Huitown" in self.graph.vertex_dict)
		self.assertEqual(1, self.graph.vertex_dict["Huitown"].city.population)
	
	def test_add_route(self):
		''' tests that when I add a route, it's actually there. '''
		dict_info = {"code":"HUI", "name":"Huitown", "country": "US", "continent": "North America", "timezone": -6, "coordinates": {"N":25, "E":25}, "population": 1, "region": 5}
		city = City(dict_info)
		vertex = Vertex("Huitown", city)
		self.graph.add_vertex(vertex)
		routes_dict = {"ports": ["HUI", "CHI"], "distance": 5000}
		self.graph.vertex_dict["Huitown"].add_route(routes_dict)
		self.assertTrue("Huitown" in self.graph.vertex_dict)
		self.assertTrue("CHI" in self.graph.vertex_dict["Huitown"].edges)
		self.assertEqual(5000,self.graph.vertex_dict["Huitown"].edges["CHI"])
		self.assertFalse("HUI" in self.graph.vertex_dict["Chicago"].edges)
		
	
	def test_remove_vertex(self):
		''' tests that when I remove a vertex, it's actually gone. '''
		vertex = self.graph.vertex_dict["Chicago"]
		self.graph.remove_vertex(vertex)
		self.assertFalse("Chicago" in self.graph.vertex_dict)
		self.assertFalse("CHI" in self.graph.vertex_dict["Mexico City"].edges)
		self.assertFalse("CHI" in self.graph.vertex_dict["Atlanta"].edges)

	def test_remove_route(self):
		''' tests that when I remove a route, it's actually gone. '''
		route = ("Miami","Washington")
		self.graph.remove_route(route)
		self.assertFalse("WAS" in self.graph.vertex_dict["Miami"].edges)
		self.assertTrue("MIA" in self.graph.vertex_dict["Washington"].edges)
		self.assertEqual(1483, self.graph.vertex_dict["Washington"].edges["MIA"])
	
	def test_parser(self):
		'''	makes sure I parsed the json file correctly. '''
		self.assertTrue("Shanghai" in self.graph.vertex_dict)
		self.assertEqual('SHA',self.graph.vertex_dict["Shanghai"].city.code)
		self.assertEqual('Shanghai', self.graph.vertex_dict["Shanghai"].city.name)
		self.assertEqual('CH', self.graph.vertex_dict["Shanghai"].city.country)
		self.assertEqual(18400000, self.graph.vertex_dict["Shanghai"].city.population)
		self.assertEqual(31, self.graph.vertex_dict["Shanghai"].city.coordinates["N"])
	
	def test_longest_flight(self):
		'''	compares what I get from get_longest_flight() with what it should be '''
		longest_flight = self.graph.get_longest_flight()
		self.assertEqual('SYD', longest_flight[0])
		self.assertEqual('LAX', longest_flight[1])
		self.assertEqual(12051, longest_flight[2])
	
	def test_shortest_flight(self):
		'''	compares what I get from get_shortest_flight() with what it should be '''
		shortest_flight = self.graph.get_shortest_flight()
		self.assertEqual('NYC', shortest_flight[0])
		self.assertEqual('WAS', shortest_flight[1])
		self.assertEqual(334, shortest_flight[2])

	def test_avg_size(self):
		'''	compares what I get from get_avg_size() with what it should be	'''
		avg_size = self.graph.get_avg_size()
		self.assertEqual(11796143, avg_size)

	def test_avg_dist(self):
		'''	compares what I get from get_avg_dist() with what it should be	'''
		avg_dist = self.graph.get_avg_distance()
		self.assertTrue(avg_dist > 2300 and avg_dist < 2301)

	def test_hub_cities(self):
		'''	compares what I get from get_hub_cities() with what it should be '''
		hub_list = self.graph.get_hub_cities()
		self.assertTrue('Istanbul' in hub_list)
		self.assertTrue('Hong Kong' in hub_list)
		self.assertEqual(2, len(hub_list))

	def test_get_cities(self):
		'''	Makes sure the number of cities is correct, and that a city that doesn't exist, isn't in the list '''
		cities_list = self.graph.get_all_cities()
		self.assertTrue(48, len(cities_list))
		self.assertTrue("Lima" in cities_list)
		self.assertFalse("aeoigheoih546" in cities_list)

	def test_get_continents(self):
		'''	compares what I get from get_continents() with what it should be '''
		continents_dict = self.graph.get_continents()
		self.assertEqual(6, len(continents_dict))
		self.assertEqual(8, len(continents_dict['Europe']))
		self.assertEqual(1, len(continents_dict['Australia']))
		self.assertEqual(6, len(continents_dict['Africa']))
		self.assertEqual(19, len(continents_dict['Asia']))
		self.assertEqual(9, len(continents_dict['North America']))
		self.assertEqual(5, len(continents_dict['South America']))
		
	if __name__=="__main__":
		unittest.main()
		 
