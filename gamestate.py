import json
from location import Location
from character import Character
from player import Player
from deck import Deck
from case_file import CaseFile
from suggestion import Suggestion
from accusation import Accusation
import random

class GameState():
    def __init__(self, game_id, player_ids, num_players, status):
        self.game_id = game_id
        self.player_ids = player_ids
        self.num_players = num_players
        self.status = status

        self.players = []   # list of player objects
        self.characters = [] # list of character objects CHANGE
        # honestly should just map character name to character object too
        # should map player id to player object too
        self.name_to_char = {} # character name to character object
        self.play_to_char = {} # player id to character object
        self.char_to_play = {} # character name to player object
        self.locations = [] # list of location objects, sorted by id
        self.turn_order = [] # list of player objects in turn order
        self.turn_index = 0   # index of player in turn order
        self.suggestions = [] # list of suggestions
        self.accusations = [] # list of accusations
        self.case_file = None # becomes actual case file object after initialization
        self._make_game_board()


    def start_game(self):
        # set up characters/players
        self.setup_players()

        # make turn order
        self.make_turn_order()

        # make solution
        self.make_solution()

        return (True, "Game has started")


    def move_player(self, player_id, location_id):
        location = self.locations[location_id]
        character = self.play_to_char[player_id]
        if player_id != self.get_turn():
            return (False, f"It is not {character.name}({player_id})'s turn")
        moved = character.move_player(location)
        if moved:
            return (moved, f"{character.name} moved to {location.location_name}") 
        return (moved, f"{character.name} could not move to {location.location_name}")
    

    def make_suggestion(self, suggester_id, suspect_name, room_id, weapon):
        suggester_char = self.play_to_char[suggester_id]
        if suggester_id != self.get_turn():
            return (False, f"It is not {suggester_char.name}({suggester_id})'s turn")
        suggester_name = suggester_char.name
        room = self.locations[room_id]

        # need to be in the same room
        if suggester_char.location != room or room.is_room == False:
            return (False, "The suggester is not in the same room suggested or the location is not a room")
        
        suggestion = Suggestion(suggester_name, suspect_name, room.location_name, weapon)
        self.suggestions.append(suggestion)
        
        # move suspect to room
        suspect_char = self.name_to_char[suspect_name]
        suspect_char.move_char(room) # need error handling maybe, but should only expect that client sends valid message
        # move weapon if we want
        self.status = "DISPROVING"
        return (True, "Suggestion is valid and was created, now in disproval process")
    

    # biggest thing is figuring how to get it in turn order with the client
    def disprove_suggestion(self, disprover, card):
        # what type is card, let's assume name for now
        suggestion = self.suggestions[-1]
        if card == suggestion.suspect or card == suggestion.room or card == suggestion.weapon:
            suggestion.set_result(disprover, True)
            self.char_to_play[suggestion.suggester].disproved_cards.append(card)
            return (True, f"{disprover} has disproved the suggestion")
        return (True, f"{disprover} did not disprove the suggestion")
        
    
    def make_accusation(self, accuser_id, suspect, room_id, weapon):
        if accuser_id != self.get_turn():
            return (False, f"It is not {self.play_to_char[accuser_id].name}({accuser_id})'s turn")
        room_name = self.locations[room_id].location_name
        accuser = self.play_to_char[accuser_id].player
        # change room name and weapon to objects
        accusation = Accusation(accuser.character, suspect, room_name, weapon)
        self.accusations.append(accusation)
        res = self.case_file.check_player_accusation(accuser, suspect, room_name, weapon)
        if res:
            accusation.set_result(True)
            self.status = "OVER"
            return (True, "Accusation was correct, game over")
        else:
            accusation.set_result(False)
            character = self.play_to_char[accuser_id]
            character.move_char(self.locations[0])
            return (True, "Accusation was incorrect, player is out of the game")
        

    def move_character(self, character_name, location_id):
        location = self.locations[location_id]
        character = self.name_to_char[character_name]
        moved = character.move_char(location)
        return moved
    

    def _make_game_board(self):
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
                    from_location.add_connected_hallway(to_location.location_id)
                elif connection['type'] == "rooms":
                    from_location.add_connected_room(to_location.location_id)
        self.locations = list(locations.values())
        self.status = "READY"
    


    def setup_players(self):
        character_starts = [("Miss Scarlett", 3), ("Col. Mustard", 7), ("Mrs. White", 19), ("Mr. Green", 17), ("Mrs. Peacock", 13), ("Professor Plum", 5)]
        random.shuffle(character_starts)
        for i in range(self.num_players):
            choice = character_starts.pop()
            player = Player(self.player_ids[i], choice[0], "READY")
            character = Character(choice[0], None, self.locations[choice[1]], player)
            self.players.append(player)
            self.name_to_char[choice[0]] = character
            self.play_to_char[self.player_ids[i]] = character
            self.char_to_play[character.name] = player
            self.characters.append(character)
        
        for unplayed in character_starts:
            character = Character(unplayed[0], None, self.locations[unplayed[1]], None)
            self.name_to_char[unplayed[0]] = character
            self.char_to_play[character.name] = None
            self.characters.append(character)
            



    def make_solution(self):
        deck = Deck()
        deck.deal(self.players)
        solution = deck.get_solution()
        self.case_file = CaseFile(solution)


    def make_turn_order(self):
        """Puts player list in turn order"""
        character_order = ["Miss Scarlett", "Col. Mustard", "Mrs. White", "Mr. Green", "Mrs. Peacock", "Professor Plum"]
        ordered_players = sorted(self.players, key=lambda player: character_order.index(player.get_character_name()))
        self.turn_order = [player.player_id for player in ordered_players]
        self.play_to_char[self.turn_order[0]].player.turn = True

    def advance_turn(self):
        self.play_to_char[self.turn_order[self.turn_index]].turn = False
        self.turn_index = (self.turn_index + 1) % self.num_players
        player_id = self.turn_order[self.turn_index]
        self.play_to_char[player_id].turn = True
        return player_id
    

    # UNUSED AS OF NOW
    def _set_player_positions(self):
        for player in self.list_of_players:
            self.player_positions[player.get_character_name()] = player.get_position()

    # might need to add this to every initial call
    def is_turn(self, player_id):
        return self.turn_order[self.turn_index]== player_id

    def get_turn(self):
        return self.turn_order[self.turn_index]

    def to_json(self):
        return {
            "game_id": self.game_id,
            "player_ids": self.player_ids,
            "num_players": self.num_players,
            "status": self.status,
            "players": [player.to_dict() for player in self.players],
            "characters": [character.to_dict() for character in self.characters],
            "name_to_char": {name: character.to_dict() for name, character in self.name_to_char.items()},
            "play_to_char": {player_id: character.to_dict() for player_id, character in self.play_to_char.items()},
            "char_to_play": {name: (player.to_dict() if player is not None else None) for name, player in self.char_to_play.items()},
            "locations": [location.to_dict() for location in self.locations],
            "turn_order": self.turn_order,
            "turn_index": self.turn_index,
            "suggestions": [suggestion.to_dict() for suggestion in self.suggestions],
            "accusations": [accusation.to_dict() for accusation in self.accusations],
            "case_file": self.case_file.to_dict() if self.case_file else None
        }

    def from_json(self, data):
        self.game_id = data["game_id"]
        self.players = data["players"]
        self.num_players = data["num_players"]
        self.status = data["status"]
        
        self.players = [Player.from_dict(p) for p in data["players"]]
        self.locations = [Location.from_dict(l) for l in data["locations"]]

        # fix this, char is referencing player so it needs to have the player that was made
        self.characters = [Character.from_dict(c) for c in data["characters"]]
        player_set = False
        for character in self.characters:
            for player in self.players:
                if character.name == player.character:
                    character.set_player(player)
                    player_set = True
            if player_set == False:
                character.set_player(None)

            for c in data["characters"]:
                if c["name"] == character.name:
                    starting_location_id = c["starting_location"]["location_id"]
                    starting_location = self.locations[starting_location_id]
                    if c["location"] is not None:
                        location_id = c["location"]["location_id"]
                        location = self.locations[location_id]
                        character.set_locations(location, starting_location)
                    else:
                        character.set_locations(None, starting_location)

        self.name_to_char = {}
        self.char_to_play = {}
        for character in self.characters:
            for player in self.players:
                if character.name == player.character:
                    self.name_to_char[character.name] = character
                    self.char_to_play[character.name] = player
        
        self.play_to_char = {}
        for player in self.players:
            for character in self.characters:
                if character.player and player.player_id == character.player.player_id:
                    self.play_to_char[player.player_id] = character

        self.turn_order = data["turn_order"]
        self.turn_index = data["turn_index"]
        self.suggestions = [Suggestion.from_dict(s) for s in data["suggestions"]]
        self.accusations = [Accusation.from_dict(a) for a in data["accusations"]]
        self.case_file = CaseFile.from_dict(data["case_file"]) if data["case_file"] else None



    def print_game_id(self):
        print(f"Game ID: {self.game_id}")
        print()

    def print_player_ids(self):
        print(f"Player IDs: {self.player_ids}")
        print()

    def print_num_players(self):
        print(f"Number of Players: {self.num_players}")
        print()

    def print_status(self):
        print(f"Status: {self.status}")
        print()

    def print_players(self):
        print("Players:")
        for player in self.players:
            print(f"  {player}")
        print()

    def print_characters(self):
        print("Characters:")
        for character in self.characters:
            print(f"  {character}")
        print()

    def print_play_to_char(self):
        print("Play to Char:")
        for player_id, character in self.play_to_char.items():
            print(f"  {player_id}: {character}")
        print()

    def print_char_to_play(self):
        print("Char to Play:")
        for char_name, player in self.char_to_play.items():
            print(f"  {char_name}: {player}")
        print()

    def print_locations(self):
        print(f"List of Locations: {self.locations}")
        print()

    def print_turn_order(self):
        print(f"Turn Order: {self.turn_order}")
        print()

    def print_turn_index(self):
        print(f"Turn Index: {self.turn_index}")
        print()

    def print_suggestions(self):
        print(f"Suggestions: {self.suggestions}")
        print()

    def print_accusations(self):
        print(f"Accusations: {self.accusations}")
        print()

    def print_case_file(self):
        print(f"Case File: {self.case_file}")
        print()

    def print_attributes(self):
        self.print_game_id()
        self.print_player_ids()
        self.print_num_players()
        self.print_status()
        self.print_players()
        self.print_characters()
        self.print_play_to_char()
        self.print_char_to_play()
        self.print_locations()
        self.print_turn_order()
        self.print_turn_index()
        self.print_suggestions()
        self.print_accusations()
        self.print_case_file()