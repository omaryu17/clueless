from location import Location
from player import Player

class Character():
    character_starts = [("Miss Scarlet", 3), ("Col. Mustard", 7), ("Mrs. White", 19), ("Mr. Green", 17), ("Mrs. Peacock", 13), ("Professor Plum", 5)]

    def __init__(self, name, location, starting_location, player):
        self.name = name    # name of character
        self.location = location    # location object
        self.starting_location = starting_location  # starting location object
        self.player = player     # player object DIFF REFERENCES CAUSES ISSUES

    def move_player(self, target_location):
        # if player exists and is ready, can only move to starting location
        if self.player and self.player.status == "READY":
            if target_location.location_id == self.starting_location.location_id:
                self.location = self.starting_location
                self.location.set_occupied()
                self.player.status = "ACTIVE"
                return True
            return False

        # otherwise, player can move to any connected location
        if target_location.is_accessible() and (target_location.location_id in self.location.connected_hallways or target_location.location_id in self.location.connected_rooms):
            # TODO: you can have more than one player in room, but not hallway
            self.location.set_occupied()
            self.location = target_location
            self.location.set_occupied()
            return True
        return False

    def move_char(self, target_location):
        # character is moved due to a suggestion
        if target_location.is_room:
            self.location = target_location
            return True
        return False
    
    def get_valid_locations(self):
        locations = []
        if self.location:
            hallways = self.location.connected_hallways
            rooms = self.location.connected_rooms
            locations = hallways + rooms
        else:
            locations = [self.starting_location.location_id]

        return locations


    def __repr__(self):
        return f"Character(name={self.name}, location={self.location}, starting_location={self.starting_location}, player={self.player})"
    
    def to_dict(self):
        res = {
            'name': self.name,
            'location': self.location.to_dict() if self.location else None,
            'starting_location': self.starting_location.to_dict(),
            'player': self.player.to_dict() if self.player else None
        }
        return res
    
    @classmethod
    def from_dict(cls, data):
        character = cls(data["name"], None, None, None)
        return character
    
    def set_locations(self, location, starting_location):
        self.location = location
        self.starting_location = starting_location
        

    def set_player(self, player):
        self.player = player
