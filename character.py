from location import Location
from player import Player

class Character():
    character_starts = [("Miss Scarlett", 3), ("Col. Mustard", 7), ("Mrs. White", 19), ("Mr. Green", 17), ("Mrs. Peacock", 13), ("Professor Plum", 5)]

    def __init__(self, name, location, starting_location, player):
        self.name = name    # name of character
        self.location = location    # location object
        self.starting_location = starting_location  # starting location object
        self.player = player     # player object

    def move_player(self, target_location):
        # if player exists and is ready, can only move to starting location
        if self.player and self.player.status == "READY":
            if target_location == self.starting_location:
                self.location = self.starting_location
                self.location.set_occupied()
                self.player.status = "ACTIVE"
                return True
            return False

        # otherwise, player can move to any connected location
        if target_location.is_accessible() and (target_location.location_id in self.location.connected_hallways or target_location.location_id in self.location.connected_rooms):
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


    def __repr__(self):
        return f"Character(name={self.name}, location={self.location}, starting_location={self.starting_location}, player={self.player})"
    
    def to_dict(self):
        return {
            'name': self.name,
            'location': self.location.to_dict() if self.location else None,
            'starting_location': self.starting_location.to_dict(),
            'player': self.player.to_dict() if self.player else None
        }
    
    @classmethod
    def from_dict(cls, data):
        character = cls(data['name'], Location.from_dict(data['location']) if data['location'] is not None else None, Location.from_dict(data['starting_location']), Player.from_dict(data['player']) if data['player'] is not None else None)
        return character