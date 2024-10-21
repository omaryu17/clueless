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

    def move_player_to_hallway(self, player_id, hallway):
        # Update the player's hallway in the game state
        self.state.locations[player_id]["hallway"] = hallway

        # Save the updated state to the database
        self.save_to_db()

    def get_player_hallway(self, player_id):
        # Return the current hallway of the player
        if player_id in self.state.locations:
            return self.state.locations[player_id].get("hallway", "unknown")
        else:
            return "unknown"

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


    # TODO: ADD OTHER METHODS


    # movement, accusation, suggestion, disprove