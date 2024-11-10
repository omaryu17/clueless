import json
import random
from location import Location
from deck import Deck
from weapon import Weapon
from case_file import CaseFile


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

        self.game_over = False
        self.winner = None


    def start_game():
        return
    
    # Set player positions
    # Scarlet is always the first character position to be set randomly, and subsequent characters are set 
    # clockwise from player Scarlet.
    def _set_player_positions(self):
        starting_locations = [self.list_of_locations[count] for count in [0, 2, 4, 12, 20, 18, 16, 8, 10]]
        room_number = random.randint(0, 8)

        for player in self.list_of_players:
            self.player_positions[player.get_character_name()] = player.move_to(starting_locations[room_number])
            if room_number == 0:
                room_number = 8
            else:
                room_number -= 1
        
        # TODO Print "Player positions have been set"
    
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
        
        self.weapon_positions = [[self.weapon_list[0], self.list_of_locations[12]], # Candlestick = location [12] Dining Room
                                 [self.weapon_list[1], self.list_of_locations[0]],  # Knife = location [0] Study
                                 [self.weapon_list[2], self.list_of_locations[16]], # Lead Pipe = location [16] Conservatory 
                                 [self.weapon_list[3], self.list_of_locations[10]], # Revolver = location [10] Billiard Room 
                                 [self.weapon_list[4], self.list_of_locations[18]], # Rope = location [18] Ballroom 
                                 [self.weapon_list[5], self.list_of_locations[20]]] # Wrench = location [20] Kitchen
        # TODO Print "Weapons have been set"


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
                #TODO print into Suggester-ONLY client  
                print("You have that card in your hand, this suggestion will be disproven. Try a different combination.")
        
        # move suspect into room of the suggester
        for player in self.list_of_players:
            if player.get_character_name() == suspect.name:
                player.move_to(suggester.get_position())
                self.player_positions[player.get_character_name()] = player.move_to(suggester.current_position)

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
                return
                # TODO print to Disprover-ONLY suggestion was disproven with { disprove_card }
                # TODO print to Suggester-ONLY that suggestion was disproven


    def disprove_suggestion(self, disprover, suspect, weapon):
        for card in disprover.hand:
            if card.name == suspect or card.name == disprover.current_position or card.name == weapon:
                return card
        return None

    # INCOMPLETE - need to make turn_order_list
    def make_accusation(self, accuser, suspect, weapon, room):
        accusation_check = self.case_file.check_player_accusation(accuser, suspect, weapon, room)
        if accusation_check:
            self.winner = accuser
            self.game_over = True
        # elif accusation_check == False and len(turn_order_list) != 1:
        #   remove accuser from turn_order_list
        # elif:
        #   self.winner = None
        #   self.game_over = True
