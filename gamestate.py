import json
from location import Location
from deck import Deck
from weapon import Weapon


class GameState():
    
    def __init__(self, game_id, list_of_players, list_of_locations):
        self.game_id = game_id
        self.list_of_players = list_of_players
        self.num_players = len(self.list_of_players)
        self.make_turn_order() # put players in turn order

        self.game_status = "RUNNING"
        self.list_of_locations = []
        self.weapon_list = []
        self._make_game_board()
        self._set_weapons()

        self.player_positions = {}
        self.weapon_positions = {}
        self._set_player_positions()
        self.suggestions = []
        self.accusations = []
        self.case_file = None
        self._set_cards_and_case_file()


    def start_game():
        return
    
    def _set_player_positions(self):
        for player in self.list_of_players:
            self.player_positions[player.get_character_name()] = player.get_position()
    
    def _make_game_board(self): # Should this be in Game?
        """Create game board from list of locations"""
        with open('game_board.json', 'r') as f:
            game_board_data = json.load(f)

        locations = {}
        for location_data in game_board_data['locations']:
            location = Location(location_id=location_data['id'], 
                                location_name=location_data['name'], 
                                is_room=location_data['room'], 
                                secret_passage=location_data.get('secret_passage', False)
                                )
            locations[location_data['name']] = location 

        # create location connections
        for connection in game_board_data['connections']:
            from_location = locations[connection['from']]
            
            for to_name in connection['to']:
                to_location = locations[to_name]
                
                if connection['type'] == "hallways":
                    from_location.add_connected_hallway(to_location)
                elif connection['type'] == "rooms":
                    from_location.add_connected_room(to_location)
        self.list_of_locations = list(locations.values())

    def _set_weapons(self): # Should this be in Game?
        with open('weapons.json', 'r') as f:
            weapons = json.load(f)

        for weapon in weapons:
            self.weapon_list.append(Weapon(weapon_id=weapon['weapon_id'],
                                      weapon_name=weapon['weapon_name'],
                                      weapon_location=weapon['weapon_location']))
        
        #TODO: Set weapons into respective locations by adding it to self.weapon_positions
        # Candlestick = location [12] Dining Room
        # Knife = location [0] Study
        # Lead Pipe = location [16] Conservatory
        # Revolver = location [10] Billiard Room
        # Rope = location [18] Ballroom
        # Wrench = location [20] Kitchen 

    def _set_cards_and_case_file(self): # Should this be in Game?
        deck = Deck()
        self.list_of_players = deck.deal(self.list_of_players)
        self.case_file = deck.solution 

    def make_turn_order(self):
        """Puts player list in turn order"""
        character_order = ["Miss Scarlett", "Colonel Mustard", "Mrs. White", "Mr. Green", "Mrs. Peacock", "Professor Plum"]

        self.list_of_players = sorted(
            self.list_of_players,
            key=lambda player: character_order.index(player.get_character_name())
        )

    # INCOMPLETE
    def make_suggestion(self, suggester, suspect, weapon):

        # check if suggester has a card that will disprove their own suggestion
        for card in suggester.hand:
            if card.name == suspect or card.name == suggester.current_position or card.name == weapon:
                print("You have that card in your hand, this suggestion will be disproven.")
        
        # move suspect into room of the suggester
        for player in self.list_of_players:
            if player.get_character_name() == suspect.name:
                player.move_to(suggester.get_position())
                # TODO update self.player_positions

        # move weapon into room of the suggester
        for weapon in self.weapon_list:
            if weapon.get_position() != suggester.get_position():
                weapon.move_to(suggester.get_position())
                # TODO update self.weapon_positions
        
        # check each player to see if they can play a card to disprove a suggestion
        for player in self.list_of_players:
            if player != suggester:
                disprove_card = self.disprove_suggestions(player, suspect, weapon)
            if disprove_card != None:
                # TODO print out that suggestion was disproven with 'disprove_card'


    def disprove_suggestion(self, disprover, suspect, weapon):
        for card in disprover.hand:
            if card.name == suspect or card.name == disprover.current_position or card.name == weapon:
                return card
        return None