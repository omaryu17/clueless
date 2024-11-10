from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class GameModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_ids = db.Column(db.JSON, nullable=False) 
    num_players = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(30), nullable=False)
    state = db.Column(db.JSON, nullable=False) 

    def __init__(self, id, player_ids, num_players, status, state):
        self.id = id
        self.player_ids = player_ids
        self.num_players = num_players
        self.status = status
        self.state = state