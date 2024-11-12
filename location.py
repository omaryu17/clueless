class Location():

    def __init__(self, location_id, location_name, is_room, secret_passage = False):
        self.location_id = location_id
        self.location_name = location_name
        self.is_room = is_room
        self.connected_hallways = []
        self.connected_rooms = []
        self.secret_passage = secret_passage
        self.occupied = False

    def is_accessible(self):
        if not self.is_room and self.occupied:
            # occupied hallways are blocked
            return False
        return True
    
    def add_connected_hallway(self, location):
        self.connected_hallways.append(location)
        
    def add_connected_room(self, location):
        self.connected_rooms.append(location)
    
    def set_occupied(self):
        self.occupied = not self.occupied

    def has_secret_passage(self):
        return self.secret_passage

    def get_name(self):
        return self.location_name
    
    def __repr__(self):
        return f"Location(id={self.location_id}, name='{self.location_name}', room={self.is_room})"
    
    def to_dict(self):
        return {
            'location_id': self.location_id,
            'location_name': self.location_name,
            'is_room': self.is_room,
            'connected_hallways': self.connected_hallways, #[location.location_id for location in self.connected_hallways],
            'connected_rooms': self.connected_rooms, #[location.location_id for location in self.connected_rooms],
            'secret_passage': self.secret_passage,
            'occupied': self.occupied
        }
    
    @classmethod
    def from_dict(cls, data):
        location = cls(data['location_id'], data['location_name'], data['is_room'], data['secret_passage'])
        location.connected_hallways = data['connected_hallways']
        location.connected_rooms = data['connected_rooms']
        location.occupied = data['occupied']
        return location