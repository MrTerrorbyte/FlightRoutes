from graph import*
from priority import*
import math

def calculate_dist(graph, route_list):
	''' accesses the edge weights of each element in the list and add them up '''
	sum = 0
	for i in range(len(route_list)-1):
		dest_code = graph.vertex_dict[route_list[i+1]].city.code
		sum += graph.vertex_dict[route_list[i]].edges[dest_code]
	
	return sum

def calculate_cost(graph, route_list):
	''' calculates the total cost of the route '''
	leg = 0
	cost = 0.0
	for i in range(len(route_list)-1):
		dest_code = graph.vertex_dict[route_list[i+1]].city.code
		cost += (0.35-(0.05*leg)) * graph.vertex_dict[route_list[i]].edges[dest_code]
		leg+=1
		if leg == 7: # after this iteration, cost will be free
			return cost
	
	return cost

def calculate_time(graph, route_list):
	''' calculates the total time it takes to travel this route '''
	acceleration = 1406.25 # km/h^2
	time = 0
	layover_time = 0
	flight_time = 0
	leg = 0	
	for i in range(len(route_list)-1):
		dest_code = graph.vertex_dict[route_list[i+1]].city.code
		dist = graph.vertex_dict[route_list[i]].edges[dest_code]
		if leg > 0:
			layover_time += 120 - 10*(len(graph.vertex_dict[route_list[i]].edges)-1)
		if dist <= 400:
			flight_time += 2*math.sqrt(dist/acceleration*60) #with no cruising. takes 200km to accel and decel
		else:
			flight_time += (2*math.sqrt(400.0/acceleration) + ((dist-400.0)/750))*60 #cruising for dist-400km, then convert to minutes
	
		leg+=1

	time = flight_time + layover_time
	return time

def dijkstra(graph, start_vertex):
	''' 
	find shortest path between start_vertex and every other path. All these
	shortest paths are stored in the dictionary called previous
	 '''
	priority_queue = PriorityQueue()
	dist = {}
	previous = {}
	dist[start_vertex] = 0
	for vertex in graph.vertex_dict:
		if vertex != start_vertex:
			dist[vertex] = float('inf') #distances start out as infinity, but are changed below
			previous[vertex] = None
		priority_queue.add(vertex, dist[vertex])

	while len(priority_queue.queue) > 0:
		vertex = priority_queue.pop_lowest()
		if dist[vertex] == float('inf'):
			break
		for edge_code in graph.vertex_dict[vertex].edges:
			short_path = dist[vertex] + graph.vertex_dict[vertex].edges[edge_code]
			edge_name = graph.find_city_name(edge_code)
			if short_path < dist[edge_name]:
				dist[edge_name] = short_path #update the distance so it reflects the shortest path
				previous[edge_name] = vertex
				priority_queue.decrease_priority(edge_name, short_path)
	
	return previous

def shortest_path(graph, start_vertex, end_vertex):
	'''
	Use dijkstra to get shortest paths. This function finds the shortest
	path from the start_vertex to the end_vertex, by using the dictionary
	given from dijkstra. I have to reverse the order.
	'''
	previous = dijkstra(graph, start_vertex)
	routes_list = []
	city = previous[end_vertex]
	while city != start_vertex:
		routes_list.append(str(city))
		city = previous[city]
	routes_list.append(start_vertex)
	ret_list = routes_list[::-1] #reverse the list
	ret_list.append(end_vertex)
	return ret_list

