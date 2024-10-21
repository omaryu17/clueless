class GameState():
    
    def __init__(self, num_players):
        self.board = [[]]
        self.num_players = num_players
        # TODO: FIGURE OUT WHAT OTHER INSTANCE VARIABLES WE NEED


    def to_json(self):
        return {"board" : f"{self.board}", "num_players" : f"{self.num_players}"}

    def from_json(self, data):
        self.board = data["board"]
        self.num_players = data["num_players"]