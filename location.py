class Location():

    def __init__(self, location_id, location_name, is_room):
        self.location_id = location_id
        self.location_name = location_name
        self.is_room = is_room
        self.connected_hallways = []
        self.connected_rooms = []
        self.secret_passage = False
        self.occupied = False

    def is_accessible(self):
        
        if (~self.is_room) & self.occupied:
            # occupied hallways are blocked
            return False
        return True
    
    def set_occupied(self):
        self.occupied = True

    def has_secret_passage(self):
        return self.secret_passage
