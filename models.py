from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class GameModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num_players = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(30), nullable=False)

    # represent state in json format probably
    state = db.Column(db.JSON, nullable=False) 

    def __init__(self, num_players, status, state):
        self.num_players = num_players
        self.status = status
        self.state = state