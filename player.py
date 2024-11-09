class Player():

    def __init__(self, player_id, name, character_name):
        self.player_id = player_id
        self.player_name = name
        self.clue_character_name = character_name
        self.hand = []
        self.current_position = None
        # TODO: self.set_initial_position() based on character name
        self.status = True
        self.turn = False

    def add_card(self, card):
        """Add Card to hand"""
        self.hand.append(card)

    def get_character_name(self):
        return self.clue_character_name
    
    def move_to(self, location):
        self.current_position = location

    def get_position(self):
        return self.current_position
    
    def get_status(self):
        return self.status
    
    def is_turn(self):
        return self.turn
    
    def make_suggestion(self, suspect, room, weapon):
        for card in self.hand:
            if card.name == suspect or card.name == room or card.name == weapon:
                print("You have that card in your hand, this suggestion will be disproven.")
        
        return suspect, room, weapon 
    
    def set_inactive(self):
        self.status = False
    
    def __repr__(self):
        return f"Player(id={self.player_id}, name='{self.player_name}', character={self.clue_character_name})"
    
    # def make_suggestion()
