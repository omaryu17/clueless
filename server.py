import eventlet
eventlet.monkey_patch()

from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy  # Import SQLAlchemy
from models import db, GameModel
from game import Game

app = Flask(__name__)
CORS(app)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'  # SQLite DB file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# later replace * with actual client url once it"s deployed

socketio = SocketIO(app, cors_allowed_origins="*")

with app.app_context():
    db.create_all()

# HTTP route for cron job to keep server alive
@app.route("/ping", methods=["GET"])
def ping():
    with app.app_context():
        return jsonify({"response": "pong active"})

# handle client connection
@socketio.on("connect")
def handle_connect():
    with app.app_context():
        print(f"Client {request.sid} connected")
        emit("server_broadcast", {"response": "Welcome to the game!"}, to=request.sid)
        emit("server_broadcast", {"response": f"Player {request.sid} has joined."}, broadcast=True)
        print("emitted")

# handle client disconnection
@socketio.on("disconnect")
def handle_disconnect():
    with app.app_context():
        print(f"Client {request.sid} disconnected")
        emit("server_broadcast", {"response": f"Player {request.sid} has disconnected."})
        print("emitted")

# handle message from client, then broadcast to all connected clients
@socketio.on("client_message")
def handle_client_message(data):
    with app.app_context():
        message = data["message"]
        print(f"Message from client {request.sid} : {message}")
        emit("server_broadcast", {"response": f"Server Broadcast - Player {request.sid} sent: {message}"}, broadcast=True)
        print("emitted")

# handle ready message from client
@socketio.on("client_ready")
def handle_client_ready(data):
    with app.app_context():
        print(f"Player {request.sid} is ready")
        emit("server_broadcast", {"response": f"Player {request.sid} is ready!"}, broadcast=True)

# Handle "Action" message from client
@socketio.on("client_action")
def handle_client_action(data):
    with app.app_context():
        print(f"Player {request.sid} performed an action")
        emit("server_broadcast", {"response": f"Player {request.sid} performed an action!"}, broadcast=True)


# Event to create a game and save it to the database
@socketio.on("create_game")
def create_game(data):
     with app.app_context():
        num_players = data.get("num_players", 2)  # Default to 2 players if not specified
        status = data.get("status", "waiting")  # Default status is 'waiting'

        # Create a new game
        new_game = Game(num_players=num_players, status=status)
        new_game.save_to_db()  # Save the game to the database

        # Print the game's info
        print(f"Game created: ID={new_game.id}, Num Players={new_game.num_players}, Status={new_game.status}")

        # Emit the game info to all connected clients
        emit("game_created", {
            "id": new_game.id,
            "num_players": new_game.num_players,
            "status": new_game.status,
            "state": new_game.state.to_json()  # Send the game state as a dictionary
        }, broadcast=True)

# Event to load a game by ID from the database
@socketio.on("get_game")
def get_game(data):
    with app.app_context():
        game_id = data.get("game_id")

        # Create a new Game instance and load the data from the database
        loaded_game = Game(num_players=0, status="inactive")  # Temporary values
        loaded = loaded_game.load_from_db(game_id)
        if loaded:
            # Print the game's info
            print(f"Game loaded: ID={loaded_game.id}, Num Players={loaded_game.num_players}, Status={loaded_game.status}")

            # Emit the loaded game info to all connected clients
            emit("game_loaded", {
                "id": loaded_game.id,
                "num_players": loaded_game.num_players,
                "status": loaded_game.status,
                "state": loaded_game.state.to_json() 
            }, broadcast=True)
        else:
            # Print the game's info
            print(f"Game with ID={loaded_game.id} could not be loaded")

            # # Emit the loaded game info to all connected clients
            # emit("game_loaded", {
            #     "id": loaded_game.id,
            #     "num_players": loaded_game.num_players,
            #     "status": loaded_game.status,
            #     "state": loaded_game.state.to_json()
            # }, broadcast=True)

# TODO: ADD MORE MESSAGE HANDLERS FOR SPECIFIC ACTIONS


if __name__ == "__main__":
    socketio.run(app, debug=True)
