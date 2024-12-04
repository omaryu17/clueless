from gamestate import GameState
from models import GameModel, db
import json

class Game():
    count = 1
    # TODO: FIGURE OUT WHAT OTHER CLASS VARIABLES WE NEED

    def __init__(self, player_ids, num_players, status):
        self.id = self.count
        self.player_ids = player_ids
        self.num_players = num_players
        self.status = status
        self.state = GameState(self.id, self.player_ids, self.num_players, self.status)
        self.count += 1


    def start_game(self):
        # players is a mapping from client_id to something
        started, msg = self.state.start_game()
        self.save_to_db()
        return (started, msg)

        # send message representing each player
        # needs to contain character, location, and cards 

    def end_game(self):
        print("Accusation was correct, game over")

    def move_player(self, player_id, location_id):
        moved, msg = self.state.move_player(player_id, location_id)
        self.save_to_db()
        return (moved, msg)

    #  not needed, exists as logic within make suggestion
    def move_character(self, character_name, location_id):
        moved, msg = self.state.move_character(character_name, location_id)
        self.save_to_db()
        return (moved, msg)

    def make_suggestion(self, suggester, suspect, room_id, weapon):
        res = self.state.make_suggestion(suggester, suspect, room_id, weapon)
        self.save_to_db()
        if res[0]:
            # allow for disprovals
            msg = res[1]
            disprover_id = res[2]
            choices = res[3]
            return (res[0], msg, disprover_id, choices)
        return (res[0], res[1])

    def disprove_suggestion(self, disprover, card):
        res = self.state.disprove_suggestion(disprover, card)
        self.save_to_db()
        return res

    def make_accusation(self, accuser, suspect, room, weapon):
        res, passed, msg = self.state.make_accusation(accuser, suspect, room, weapon)
        self.save_to_db()
        if res and passed and self.state.status == "OVER":
            self.end_game()
            return (res, passed, msg)
        elif res and not passed:
            return (res, passed, msg)
        return res, msg

    def end_turn(self):
        turn, msg = self.state.advance_turn()
        self.save_to_db()
        return (turn, f"It is now {msg}'s turn")
    
    def get_valid_locations(self, player_id):
        """Get list of rooms player can travel to"""
        res = self.state.get_valid_locations(player_id)
        return res           

    def get_valid_moves(self, player_id):
        """Get list of valid moves player can make"""
        res = self.state.get_valid_moves(player_id)
        return res 
    
    def valid_end_turn(self, player_id):
        """Get whether player can end turn"""
        res = self.state.valid_end_turn(player_id)
        return res

    def save_to_db(self):
        model = GameModel.query.get(self.id) if self.id else None
        if model:
            model.player_ids = json.dumps(self.player_ids)
            model.num_players = self.num_players
            model.status = self.status
            model.state = self.state.to_json()
        else:
            model = GameModel(self.id, json.dumps(self.player_ids), self.num_players, self.status, self.state.to_json())
            db.session.add(model)
        db.session.commit()
        self.id = model.id
        print(f"Game saved with id {self.id}")


    def load_from_db(self, id):
        model = GameModel.query.get(id)
        if model:
            self.id = model.id
            self.player_ids = json.loads(model.player_ids)
            self.num_players = model.num_players
            self.status = model.status
            self.state = GameState(-1, self.player_ids, self.num_players, self.status)
            self.state.from_json(model.state)
            print(f"Game loaded with id {self.id}")
            return True
        else:
            print(f"Failed to load game with id {id}")
            return False