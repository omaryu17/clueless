from gamestate import GameState

class Game():
    count = 0
    # TODO: FIGURE OUT WHAT OTHER CLASS VARIABLES WE NEED

    def __init__(self, num_players, status):
        self.id = 0
        self.num_players = num_players
        self.status = status
        self.state = GameState(num_players)
        # TODO: FIGURE OUT WHAT OTHER INSTANCE VARIABLES WE NEED

    # TODO: ADD OTHER METHODS TO COMMUNICATE WITH SERVER

