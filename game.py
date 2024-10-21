from gamestate import GameState
from models import GameModel, db

class Game():
    count = 0
    # TODO: FIGURE OUT WHAT OTHER CLASS VARIABLES WE NEED

    def __init__(self, num_players, status):
        self.id = self.count
        self.num_players = num_players
        self.status = status
        self.state = GameState(num_players)
        # TODO: FIGURE OUT WHAT OTHER INSTANCE VARIABLES WE NEED
        self.count += 1

    def save_to_db(self):
        model = GameModel(self.num_players, self.status, self.state.to_json())
        db.session.add(model)
        db.session.commit()
        self.id = model.id
        print(f"Game saved with id {self.id}")


    def load_from_db(self, id):
        model = GameModel.query.get(id)
        if model:
            self.id = model.id
            self.num_players = model.num_players
            self.status = model.status
            self.state = GameState(self.num_players)
            self.state.from_json(model.state)
            print(f"Game loaded with id {self.id}")
            return True
        else:
            print(f"Failed to load game with id {id}")
            return False


    # TODO: ADD OTHER METHODS TO COMMUNICATE WITH SERVER


    # movement, accusation, suggestion, disprove