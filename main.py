from graph import *
import json
import sys
import webbrowser
import calculations

json_file = open("map_data.json")
json_file2 = open("cmi_hub.json")
json_data2 = json.load(json_file2)
json_data = json.load(json_file)
json_file.close()
json_file2.close()
graph = Graph()
json_data["metros"] += json_data2["metros"]
json_data["routes"] += json_data2["routes"]


graph = graph.construct_json_graph(json_data["metros"], json_data["routes"])
url = graph.get_url()


def exit_state():
	'''
	When exiting, print the url to the visual map then exit.
	'''
	webbrowser.open_new_tab(url)
	#print '\n'+url
	sys.exit()	


def city_state():
	'''	In this state, you can either select a city and view its information, exit, or view the statistical info about CSAir. '''
	cities_list = graph.get_all_cities()
	cities_list = sorted(cities_list)
	count = 1
	for index in range(0, len(cities_list)):
		print count,':', cities_list[index]
		count += 1

	input_text = raw_input("Type in a city's number to view more information about it. Type in -9 to exit program\n")
	while (input_text.isdigit() and (int(input_text) > len(cities_list) or int(input_text) < 1)) or input_text.isdigit() == False:
		if input_text == '-9':
			exit_state()
		print "Sorry. Your request cannot be understood."
		input_text = raw_input("Type in a city's number to view more information about it. Type in -9 to exit program\n")
	
	input_num = int(input_text)-1
	graph.vertex_dict[cities_list[input_num]].city.print_city_info()  #prints the info about a city
	print "adjacent cities:",
	for edgeCode in graph.vertex_dict[cities_list[input_num]].edges:
		print edgeCode+"-"+str(graph.vertex_dict[cities_list[input_num]].edges[edgeCode]),  #prints the adjacent cities
	print '\n'
	start_state()

def edit_state():
    ''' state where the user can edit a city '''
    cities_list = graph.get_all_cities()
    cities_list = sorted(cities_list)
    count = 1
    for index in range(0, len(cities_list)):
        print count,':', cities_list[index]
        count += 1

    input_text = raw_input("Type in a city's number to edit information about it. Type in -9 to exit program\n")
    while (input_text.isdigit() and (int(input_text) > len(cities_list) or int(input_text) < 1)) or input_text.isdigit() == False:
        if input_text == '-9':
            exit_state()
        print "Sorry. Your request cannot be understood."
        input_text = raw_input("Type in a city's number to view more information about it. Type in -9 to exit program\n")
    
    if input_text == '-9':
        exit_state()
    print "Choose what you want to edit by typing in the number corresponding to the info you wish to change, or type in -9 to exit program\n"
    option = raw_input("\n1.name\n2.code\n3.country\n4.continent\n5.timezone\n6.coordinates\n7.population\n8.region\n9.routes\n")
    while option.isalpha() or (int(option) not in range(1,10) and option != '-9'):
        print "Sorry. Your request cannot be understood."
        option = raw_input("Choose what you want to edit by typing in the number corresponding to the info you wish to change")

    if option == '-9':
        exit_state()

    input_num = int(input_text)-1
    option = int(option)
    
    if option == 1:
	    graph.vertex_dict[cities_list[input_num]].edit_name(graph)
	
    elif option == 2:
        graph.vertex_dict[cities_list[input_num]].edit_code(graph)

    elif option == 3:
        graph.vertex_dict[cities_list[input_num]].edit_country()
    
    elif option == 4:
        graph.vertex_dict[cities_list[input_num]].edit_continent()

    elif option == 5:
        graph.vertex_dict[cities_list[input_num]].edit_timezone()

    elif option == 6:
        graph.vertex_dict[cities_list[input_num]].edit_coordinates()

    elif option == 7:
        graph.vertex_dict[cities_list[input_num]].edit_population()

    elif option == 8:
        graph.vertex_dict[cities_list[input_num]].edit_region()

    elif option == 9:
        graph.vertex_dict[cities_list[input_num]].edit_routes(graph)
	
	start_state()

def add_route_state():
	'''adds a route to the graph '''
	source = raw_input("Type in the name of the city that you want to start from or type in -9 to exit the program\n")
	while source not in graph.vertex_dict and source != '-9':
		print "City not found"
		source = raw_input("Type in the name of the city you want to start from or type in -9 to exit the program\n")
	
	if source == '-9':
		exit_state()
	
	dest = raw_input("Type in the name of the destination or type in -9 to exit the program\n")
	while dest not in graph.vertex_dict and dest != '-9':
		print "City not found"
		source = raw_input("Type in the name of the destination or type in -9 to exit the program\n")

	if source == '-9':
		exit_state()

	dist = raw_input("Type in the distance between the source city and the destination city or type in -9 to exit the program\n")
	while dist.isdigit() == False or (dist.isdigit() and int(dist) < 0 and dist != '-9'):
		print "Sorry. Your request cannot be understood."
		dist = raw_input("Type in the distance between the source city and the destination city or type in -9 to exit the program\n")

	if source == '-9':
		exit_state()

	source_code = graph.vertex_dict[source].city.code
	dest_code = graph.vertex_dict[dest].city.code
	route_dict = {"ports": [source_code,dest_code], "distance": dist}
	graph.vertex_dict[source].add_route(route_dict)

def remove_route_state():
	'''removes a route '''
	source = raw_input("Type in the name of the city that you want to start from or type in -9 to exit the program\n")
	while source not in graph.vertex_dict and source != '-9':
		print "City not found"
		source = raw_input("Type in the name of the city you want to start from or type in -9 to exit the program\n")
	
	if source == '-9':
		exit_state()
	
	dest = raw_input("Type in the name of the destination or type in -9 to exit the program\n")
	while dest not in graph.vertex_dict and dest != '-9':
		print "City not found"
		source = raw_input("Type in the name of the destination or type in -9 to exit the program\n")

	if source == '-9':
		exit_state()

	route = (source, dest)
	graph.remove_route(route)
	

def remove_city_state():
	'''removes the vertex+city from the graph '''
	vertex_name = raw_input("Type in the name of the city you want to remove or type in -9 to exit the program\n")
	while vertex_name not in graph.vertex_dict and vertex_name != '-9':
		print "City not found."
		vertex_name = raw_input("Type in the name of the city you want to remove or type in -9 to exit the program\n")
	
	if vertex_name == '-9':
		exit_state()

	graph.remove_vertex(graph.vertex_dict[vertex_name])
	start_state()

def add_city_state():
	'''add vertex+city to the graph '''
	dict_info = {"code":"", "name":"", "country": "", "continent": "", "timezone": None, "coordinates": {}, "population": 0, "region": 0}
	city = City(dict_info)
	vertex = Vertex("temp", city)
	graph.add_vertex(vertex)
	
	if vertex.edit_name(graph) == -1:
		graph.remove_vertex(vertex)
		start_state()
	if vertex.edit_code(graph) == -1:
		graph.remove_vertex(vertex)
		start_state()
	if vertex.edit_country() == -1:
		graph.remove_vertex(vertex)
		start_state()
	if vertex.edit_continent() == -1:
		graph.remove_vertex(vertex)
		start_state()
	if vertex.edit_timezone() == -1:
		graph.remove_vertex(vertex)
		start_state()
	if vertex.edit_coordinates() == -1:
		graph.remove_vertex(vertex)
		start_state()
	if vertex.edit_population() == -1:
		graph.remove_vertex(vertex)
		start_state()
	if vertex.edit_region() == -1:
		graph.remove_vertex(vertex)
		start_state()
	if vertex.edit_routes(graph) == -1:
		start_state()

	start_state()

def save_state():
	''' saves the current graph as a json file '''
	json_dict = {"data sources": json_data["data sources"]}
	json_dict["metros"] = []
	json_dict["routes"] = []
	city_info = {}
	route_info = []

	for vertex in graph.vertex_dict:
		curr_vertex = graph.vertex_dict[vertex]
		
		city_info = {}
		route_info = []

		city_info["code"] = curr_vertex.city.code
		city_info["name"] = curr_vertex.city.name
		city_info["country"] = curr_vertex.city.country
		city_info["continent"] = curr_vertex.city.continent
		city_info["timezone"] = curr_vertex.city.timezone
		city_info["coordinates"] = curr_vertex.city.coordinates
		city_info["population"] = curr_vertex.city.population
		city_info["region"] = curr_vertex.city.region
		
		for edge_code in curr_vertex.edges:
			route_dict= {"ports":[curr_vertex.city.code, edge_code], "distance": curr_vertex.edges[edge_code]}
			route_info.append(route_dict)

		json_dict["metros"].append(city_info)
		json_dict["routes"].append(route_info)
	
	json_str = json.dumps(json_dict, indent=4, sort_keys=True)
	json_file = open("saved.json", "w")
	json_file.write(json_str)
	
	start_state()

def route_info_state():
	''' get a route from the user. Store it in a list. Then calculate cost, distance, time '''
	route_list = []
	input_text = raw_input("Type in the city you wish to start from or -9 to exit\n")
	while input_text not in graph.vertex_dict and input_text != '-9':
		print "Sorry, your request cannot be understood."
		input_text = raw_input("Type in the city you wish to start form or -9 to exit\n")
	
	if input_text == '-9':
		exit_state()

	route_list.append(input_text)

	vertices = graph.vertex_dict
	while 1 > 0:
		input_text = raw_input("Type in your following routes one at a time and separate each with a new line. Type in 0 when you're done or -9 to exit\n")
		prev_city_name = route_list[len(route_list)-1]
		prev_edges = vertices[prev_city_name].edges
		while input_text != '0' and input_text != '-9' and((input_text not in vertices) or (graph.vertex_dict[input_text].city.code not in prev_edges)):
			if input_text in vertices and graph.vertex_dict[input_text].city.code not in prev_edges:
				print "Sorry, from your previously listed city, you cannot fly to your current selection.\n"
				print "You can only go to these cities. Please print their full names.\n",prev_edges
				input_text = raw_input("Please type in a different city\n")
				continue
			print "Sorry, your request cannot be understood."
			input_text = raw_input("Type in your following routes one at a time and separate each with with a new line. Type in 0 when you're done or -9 to exit\n")
		if input_text == '-9':
			exit_state()

		if input_text == '0':
			break
		route_list.append(input_text)
		print "Your current route is",route_list
	
	print "Your final route is",route_list
	print "The total distance of your route is",calculations.calculate_dist(graph, route_list), "kilometers"
	print "The total cost of your route is", calculations.calculate_cost(graph, route_list), "dollars"
	print "The total time of your route is", calculations.calculate_time(graph, route_list), "minutes"

def shortest_route_state():
	''' uses dijkstra's algorithm '''
	start = raw_input("Type in the city name you wish to start from or type in -9 to exit\n")
	while start != '-9' and start not in graph.vertex_dict:
		print "There is no city by that name."
		start = raw_input("Type in the city name you wish to start from or type in -9 to exit\n")
	
	if start == '-9':
		exit_state()

	dest = raw_input("Type in the city name you wish to end at or type in -9 to exit\n")
	while dest != '-9' and dest not in graph.vertex_dict:
		print "There is no city by that name."
		dest = raw_input("Type in the city name you wish to end at or type in -9 to exit\n")

	if dest == '-9':
		exit_state()
	
	route_list = calculations.shortest_path(graph, start, dest)
	print "\nThe shortest route is", route_list
	print "The total distance of your route is", calculations.calculate_dist(graph, route_list), "kilometers"
	print "The total cost of your route is", calculations.calculate_cost(graph, route_list), "dollars"
	print "The total time of your route is", calculations.calculate_time(graph, route_list), "minutes\n"
	start_state()
	

def start_state():
	''' the initial state is where all the other states are connected to '''
	while(1 > 0):
		input_text = ""
		print "Welcome to CSAir!\n\n"
		print "Type in the number corresponding to the option"
		print "1.About CSAir\n2.View Cities\n3.Edit City\n4.Add City\n5.Add Route"
		input_text = raw_input("6.Remove City\n7.Remove Route\n8.Save as json\n9.Get Route Info\n10.Find Shortest Route\n11.Exit\n")
		
		# if the input_text is not a recognized command, prompt the user for input again.
		while input_text.isdigit() == False or int(input_text) > 11 or int(input_text) < 1: 
			print "Sorry. Your request cannot be understood."
			print "Type in the number corresponding to the option"
			print "1.About CSAir\n2.View Cities\n3.Edit City\n4.Add City\n5.Add Route"
			input_text = raw_input("6.Remove City\n7.Remove Route\n8.Save as json\n9.Get Route Info\n10.Find Shortest Route\n11.Exit\n")
		
		input_num = int(input_text)

		if input_num == 1:
			graph.print_stats()

		elif input_num == 2:
			city_state()
		
		elif input_num == 3:
			edit_state()
			
		elif input_num == 4:
			add_city_state()
			
		elif input_num == 5:
			add_route_state()
			
		elif input_num == 6:
			remove_city_state()
			
		elif input_num == 7:
			remove_route_state()
		
		elif input_num == 8:
			save_state()

		elif input_num == 9:
			route_info_state()

		elif input_num == 10:
			shortest_route_state()

		elif input_num == 11:
			exit_state()		

start_state()
