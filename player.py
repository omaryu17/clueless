from card import Card

class Player():

    def __init__(self, player_id, character, status):
        self.player_id = player_id
        self.character = character
        self.status = status
        self.hand = []
        self.turn = False
        self.disproved_cards = []

    def add_card(self, card):
        """Add Card to hand"""
        self.hand.append(card)

    def get_character_name(self):
        return self.character

    def get_position(self):
        return self.current_position
    
    def get_status(self):
        return self.status
    
    def is_turn(self):
        return self.turn
    
    def set_inactive(self):
        self.status = "OUT"
    
    def __repr__(self):
        return f"Player(id={self.player_id}, character={self.character}, status={self.status}, hand={self.hand}, turn={self.turn}, disproved_cards={self.disproved_cards})"
    
    def to_dict(self):
        return {
            'player_id': self.player_id,
            'character': self.character,
            'status': self.status,
            'hand': [card.to_str() for card in self.hand],
            'turn': self.turn,
            'disproved_cards': self.disproved_cards
        }
    
    @classmethod
    def from_dict(cls, data):
        player = cls(data['player_id'], data['character'], data['status'])
        player.hand = [Card.from_str(card) for card in data['hand']]
        player.turn = data['turn']
        player.disproved_cards = data['disproved_cards']
        return player

