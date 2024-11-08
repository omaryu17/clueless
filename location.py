class Location():

    def __init__(self, location_id, location_name, is_room, secret_passage = False):
        self.location_id = location_id
        self.location_name = location_name
        self.is_room = is_room
        self.connected_hallways = []
        self.connected_rooms = []
        self.secret_passage = secret_passage
        self.occupied = False
        self.weapon = None

    def is_accessible(self):
        
        if (~self.is_room) & self.occupied:
            # occupied hallways are blocked
            return False
        return True
    
    def add_connected_hallway(self, location):
        self.connected_hallways.append(location)
        
    def add_connected_room(self, location):
        self.connected_rooms.append(location)
    
    def set_occupied(self):
        self.occupied = True

    def has_secret_passage(self):
        return self.secret_passage

    def get_name(self):
        return self.location_name
    
    def set_weapon(self, weapon):
        self.weapon = weapon
    
    def __repr__(self):
        return f"Location(id={self.location_id}, name='{self.location_name}', room={self.is_room})"
