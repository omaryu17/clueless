class Weapon():

    def __init__(self, weapon_id, weapon_name, weapon_location):
        self.weapon_id = weapon_id
        self.weapon_name = weapon_name
        self.weapon_location = weapon_location
        
    def get_position(self):
        return self.weapon_location
    
    def get_name(self):
        return self.weapon_name
    
    def move_to(self, location):
        self.weapon_location = location
    
    def check_player_accusation(self, accuser, suspect, room, weapon):
        return
        #TODO create method 