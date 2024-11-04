class CaseFile():

    def __init__(self, suspect, weapon, room):
        self.suspect = suspect
        self.weapon = weapon
        self.room = room

    def check_player_accusation(self, player, suspect, weapon, room):
        if (suspect == self.suspect) & (weapon == self.weapon) & (room == self.room):
            # TODO: update game/gamestate
            return 
        else: 
            player.set_inactive()