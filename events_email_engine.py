from uuid import uuid4
from collections import defaultdict

class Event:
	def __init__(self, events):
		self.id = str(uuid4())[:5]
		self.categories = {}
		for e in events:
			self.categories[e] = True

	def add_category(self, category):
		self.categories[category] = True
  
	def __str__(self):
		return f"Event: ID {str(self.id)[:5]} and cats: {', '.join(self.categories.keys())}"

class User:
    def __init__(self, fav_categories):
        self.id = str(uuid4())[:5]
        self.fav_categories = {}
        for cat in fav_categories:
            self.fav_categories[cat] = True
    
    def __str__(self):
        return f"User: ID {str(self.id)[:5]} and cats: {', '.join(self.fav_categories.keys())}"
    

class StubHub:
    def __init__(self, events, users):
        self.events = {} # key is UUID, value is event object
        for event in events:
            self.events[event.id] = event
        
        self.users = {}
        for user in users:
            self.users[user.id] = user
        
        self.event_categories = defaultdict(list) # key is a category, value is a list of event ids
        self.user_categories = defaultdict(list)
        self.recs = set()
        self.process()
    
    def process(self):
        # processes all recs from 0
        self.recs = set()
        
        # make user cats
        for user in self.users.values():
            for user_cat in user.fav_categories.keys():
                self.user_categories[user_cat].append(user.id)
                
        # make event cats
        for event in self.events.values():
            for event_cat in event.categories.keys():
                self.event_categories[event_cat].append(event.id)
                
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
            
    
	# TODO: add_event and add_user, and send_emails and some in-memory-store of sent emails
 
    def add_event(self, event):
        # add an event
        self.events[event.id] = event
        
        # update recs
        for event_cat in event.categories:
            for user_id in self.user_categories[event_cat]:
                self.recs.add((event.id, user_id))
            
    def add_user(self, user):
        # add a user
        self.users[user.id] = user
        
        # update recs
        for user_cat in user.fav_categories:
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


# main
# # TODO: location
engine = StubHub(
	[
     Event(['rock', 'pop']),
     Event(['rap']),
	],
	[
     User(['rock', 'folk']),
     User(['rock', 'pop'])
	]
)

engine.add_event(Event(['folk']))
engine.add_user(User(['rap']))

engine.print_events()
engine.print_users()

# print(engine.event_categories)
# print(engine.user_categories)
engine.print_recs()