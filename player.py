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
