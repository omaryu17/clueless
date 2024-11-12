from card import Card

class CaseFile():

    def __init__(self, solution):
        self.solution = solution
        for card in solution:
            if card.card_type == "suspect":
                self.suspect = card
            elif card.card_type == "weapon":
                self.weapon = card
            elif card.card_type == "room":        
                self.room = card    

    def check_player_accusation(self, player, suspect, room, weapon):
        if (suspect == self.suspect.name) and (room == self.room.name) and (weapon == self.weapon.name):
            return True
        else: 
            player.set_inactive()
            return False

    def __repr__(self):
        return f"CaseFile(suspect={self.suspect}, weapon={self.weapon}, room={self.room})"
    

    def to_dict(self):
        return {
            'solution': [card.to_str() for card in self.solution]
        }
    
    @classmethod
    def from_dict(cls, data):
        solution = [Card.from_str(card) for card in data['solution']]
        return cls(solution)