from gamestate import GameState
from models import GameModel, db
import json

class Game():
    count = 0
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
        res = self.state.start_game()
        self.save_to_db()
        return res

        # send message representing each player
        # needs to contain character, location, and cards 

    def end_game(self):
        print("Accusation was correct, game over")

    def move_player(self, player_id, location_id):
        res = self.state.move_player(player_id, location_id)
        self.save_to_db()

    #  not needed, exists as logic within make suggestion
    def move_character(self, character_name, location_id):
        moved, is_room = self.state.move_character(character_name, location_id)
        if moved and is_room:
            # allow for additional action, i.e. suggestion/accusation
            pass
        self.save_to_db()

    def make_suggestion(self, suggester, suspect, room_id, weapon):
        res = self.state.make_suggestion(suggester, suspect, room_id, weapon)
        if res:
            # allow for disprovals
            pass
        self.save_to_db()
        pass

    def disprove_suggestion(self, disprover, card):
        res = self.state.disprove_suggestion(disprover, card)
        if res:
            # was disproved
            pass
        else:
            # not disproved, continue disapprovals
            pass
        self.save_to_db()
        pass

    def make_accusation(self, accuser, suspect, room, weapon):
        res = self.state.make_accusation(accuser, suspect, room, weapon)
        if res:
            self.end_game()
            return res
        self.save_to_db()
        return res

    def end_turn(self):
        turn = self.state.advance_turn()
        self.save_to_db()
        # return turn to client
        pass
            

    def save_to_db(self):
        model = GameModel.query.get(self.id) if self.id else None
        if model:
            model.player_ids = json.dumps(self.players_ids)
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