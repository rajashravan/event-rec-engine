from uuid import uuid4
from collections import defaultdict
from random import randrange

GRID_SIZE = 10

class Event:
	def __init__(self, categories, lat=None, lon=None):
		self.id = str(uuid4())[:5]
		self.categories = {}
		for e in categories:
			self.categories[e] = True

		if not lat:
			lat = randrange(GRID_SIZE)
		if not lon:
			lon = randrange(GRID_SIZE)
		
		self.lat = lat
		self.lon = lon
		
	def add_category(self, category):
		self.categories[category] = True
	
	def __str__(self):
		return f"Event: ID {str(self.id)[:5]} and cats: {', '.join(self.categories.keys())}. Coords: {self.lat}, {self.lon}"

class User:
	def __init__(self, fav_categories, lat=None, lon=None):
		self.id = str(uuid4())[:5]
		self.fav_categories = {}
		for cat in fav_categories:
			self.fav_categories[cat] = True
	 
		if lat is None:
			lat = randrange(10)
		if lon is None:
			lon = randrange(10)
		
		self.lat = lat
		self.lon = lon
	
	def __str__(self):
		return f"User: ID {str(self.id)[:5]} and cats: {', '.join(self.fav_categories.keys())}. Coords: {self.lat}, {self.lon}"
	

class StubHub:
	def __init__(self, events, users):
		self.events = {} # key is UUID, value is event object
		for event in events:
			self.events[event.id] = event
		
		self.users = {}
		for user in users:
			self.users[user.id] = user
		
		self.event_categories = defaultdict(set) # key is a category, value is a list of event ids
		self.user_categories = defaultdict(set)
		self.recs = set()
		self.sent_messages = set()
		self.process()

		self.make_event_location_grid()
	
	def make_event_location_grid(self):
		self.event_location_grid = defaultdict(lambda: defaultdict(set))
		
		for event in self.events.values():
			self.add_event_to_grid(event)
		 
	
	def add_event_to_grid(self, event):
		self.event_location_grid[event.lat][event.lon].add(event.id)
	
	def find_nearby_events_for_user(self, user):
		user_x = user.lat
		user_y = user.lon

		nearby_events = []

		start_x = user_x - 1
		end_x = user_x + 1

		start_y = user_y - 1
		end_y = user_y + 1

		for x in range(start_x, end_x+1):
			for y in range(start_y, end_y+1):
				for event_id in self.event_location_grid[x][y]:
					nearby_events.append(event_id)
		
		print("Nearby events for user " + user.id)
		print(nearby_events)

	
	def process(self):
		# processes all recs from 0
		self.recs = set()
		
		# make user cats
		for user in self.users.values():
			for user_cat in user.fav_categories.keys():
				self.user_categories[user_cat].add(user.id)
				
		# make event cats
		for event in self.events.values():
			for event_cat in event.categories.keys():
				self.event_categories[event_cat].add(event.id)
				
		# match recos
		for event_cat, event_ids in self.event_categories.items():
			# event_cat is a string
			# events are list of IDs
			
			# find matching users
			if event_cat not in self.user_categories:
				continue
				
			matching_user_ids = self.user_categories[event_cat]
			for user_id in matching_user_ids:
				for event_id in event_ids:
					self.recs.add((event_id, user_id))
 
	def add_event(self, event):
		# add an event
		self.events[event.id] = event

		# add to grid
		self.add_event_to_grid(event)
		
		# update recs
		for event_cat in event.categories:
			self.event_categories[event_cat].add(event.id)
			for user_id in self.user_categories[event_cat]:
				self.recs.add((event.id, user_id))
			
	def add_user(self, user):
		# add a user
		self.users[user.id] = user
		
		# update recs
		for user_cat in user.fav_categories:
			self.user_categories[user_cat].add(user.id)
			for event_id in self.event_categories[user_cat]:
				self.recs.add((event_id, user.id))
	
	def print_events(self):
		for event in self.events.values():
			print(event)
		print("")
	
	def print_users(self):
		for user in self.users.values():
			print(user)
		print("")
	
	def print_recs(self):
		for rec in self.recs:
			print(rec)
	
	def print_event_location_grid(self):
		for row_index in range(GRID_SIZE):
			for col_index in range(GRID_SIZE):
				events_at_location = self.event_location_grid[row_index][col_index]
				if not events_at_location:
					continue
				print(f"Events at Lat {row_index} and Lon {col_index}:")
				for event in events_at_location:
					print(event)

	
	def send_messages(self):
		# send messages based on recs
		for rec in self.recs:
			if rec in self.sent_messages:
				continue
			self.sent_messages.add(rec)
			event_id = rec[0]
			user_id = rec[1]
			print(f"Recing event {event_id} to {user_id}")


# main
# # TODO: location, birthday

origin_user = User([], 0, 0)

engine = StubHub(
	[
	 Event(['rock', 'pop']),
	 Event(['rap'], 1, 1),
	],
	[
	 User(['rock', 'folk']),
	 User(['rock', 'pop']),
	 origin_user
	]
)

engine.add_event(Event(['folk']))
engine.add_user(User(['rap']))

engine.add_event(Event(['unknown_cat_1']))
engine.add_user(User(['unknown_cat_2']))

engine.print_events()
engine.print_users()

# print(engine.event_categories)
# print(engine.user_categories)
engine.send_messages()
engine.send_messages()

engine.print_event_location_grid()

engine.find_nearby_events_for_user(origin_user)