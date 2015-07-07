class PriorityQueue(object):
	
	def __init__(self):
		''' declares a dictionary as a member variable '''
		self.queue = {}
	
	def pop_lowest(self):
		''' 
		pops the element with the lowest priority value. Each element
		is a key-value pair where the key is a name (city name) and the
		value is the priority
		'''
		lowest_elem = None
		lowest = float('inf')
		for key in self.queue:
			if self.queue[key] < lowest or lowest_elem == None:
				lowest = self.queue[key]
				lowest_elem = key
			
		name = lowest_elem
		self.queue.pop(lowest_elem)
		return name

	def add(self, name, priority):
		''' adds the given name and priority into the dictionary '''
		self.queue[name] = priority

	def decrease_priority(self, name, priority):
		''' 
		Finds the key with the given name, and change its priority
		to the priority value given.
		'''
		for key in self.queue:
			if key == name:
				self.queue[key] = priority
				return
