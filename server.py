import eventlet
eventlet.monkey_patch()

from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from models import db
from game import Game
import json

app = Flask(__name__)
CORS(app)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'  # SQLite DB file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# later replace * with actual client url once it"s deployed

#socketio = SocketIO(app, cors_allowed_origins="*", async_mode="gevent", ping_interval=5, ping_timeout=10)
socketio = SocketIO(app, cors_allowed_origins="*")#, async_mode="gevent", ping_interval=5, ping_timeout=10)

with app.app_context():
    db.drop_all()
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
        status = data.get("status", "READY")  # Default status is 'waiting'

        # Get list of all connected client SIDs
        player_ids = [client for client in socketio.server.manager.rooms['/'].keys() if client != None]
        print(f"Connected clients: {player_ids}")


        # Create a new game
        new_game = Game(player_ids=player_ids, num_players=int(num_players), status=status)

        # Start new game
        res = new_game.start_game()
        print(f"Game started: {res}")

        #new_game.save_to_db()  # Save the game to the database

        # Print the game's info
        print(f"Game created: ID= {new_game.id}, Player IDs= {new_game.player_ids}, Num Players= {new_game.num_players}, Status= {new_game.status}, State= {new_game.state}")

        # Emit the game info to all connected clients
        emit("game_created", {
            "id": new_game.id,
            "player_ids": json.dumps(new_game.player_ids),
            "num_players": new_game.num_players,
            "status": new_game.status,
            "state": new_game.state.to_json()  # Send the game state as a dictionary
        }, broadcast=True)


# Event to move a player to a new location
@socketio.on("move_player")
def move_player(data):
    with app.app_context():
        player_id = request.sid
        game_id = data.get("game_id")
        location_id = data.get("location_id")
        loaded_game = load_from_db(game_id)
        if loaded_game:
            res = loaded_game.move_player(player_id, int(location_id))
            print(f"RES: {res}")
            if res[0]:
                print(res[1])
                # NEED TO FIND A WAY TO GIVE CLIENT A READABLE STATE OF THE GAME SO IT CAN UPDATE ITS VIEWS
                emit("player_moved", {
                    "game_id": game_id,
                    "player_id": player_id,
                    "location_id": location_id,
                    "state": loaded_game.state.to_json()
                }, broadcast=True)
            else:
                emit("player_move_error", {"game_id": game_id}, broadcast=True)
        else:
            emit("Could not load game", {"game_id": game_id}, broadcast=True)

# Event to make a suggestion
@socketio.on("make_suggestion")
def make_suggestion(data):
    with app.app_context():
        player_id = request.sid
        game_id = data.get("game_id")
        suspect = data.get("suspect")
        room_id = data.get("room_id")
        weapon = data.get("weapon")
        loaded_game = load_from_db(game_id)
        if loaded_game:
            res = loaded_game.make_suggestion(player_id, suspect, room_id, weapon)
            if res[0]:
                # res[1] -> msg
                # res[2] -> disprover_id
                # res[3] -> choices
                emit("suggestion_made", {
                    "game_id": game_id,
                    "suggester": player_id,
                    "suspect": suspect,
                    "room_id": room_id,
                    "weapon": weapon,
                    "state": loaded_game.state.to_json(),
                    "disprover_id": res[2],
                    "choices": json.dumps(res[3])
                }, broadcast=True)
            else:
                emit("suggestion_error", {"game_id": game_id}, broadcast=True)
        else:
            emit("Could not load game", {"game_id": game_id}, broadcast=True)

# Event to disprove a suggestion
@socketio.on("disprove_suggestion")
def disprove_suggestion(data):
    with app.app_context():
        player_id = request.sid
        game_id = data.get("game_id")
        card = data.get("card")
        loaded_game = load_from_db(game_id)
        if loaded_game:
            res = loaded_game.disprove_suggestion(player_id, card)
            if res:
                emit("suggestion_disproved", {
                    "game_id": game_id,
                    "disprover": player_id,
                    "card": card,
                    "state": loaded_game.state.to_json()
                }, broadcast=True)
            else:
                emit("disprove_error", {"game_id": game_id}, broadcast=True)
        else:
            emit("Could not load game", {"game_id": game_id}, broadcast=True)

# Event to make an accusation
@socketio.on("make_accusation")
def make_accusation(data):
    with app.app_context():
        player_id = request.sid
        game_id = data.get("game_id")
        suspect = data.get("suspect")
        room_id = data.get("room_id")
        weapon = data.get("weapon")
        loaded_game = load_from_db(game_id)
        if loaded_game:
            res = loaded_game.make_accusation(player_id, suspect, room_id, weapon)
            if res[0]:
                print(res[1])
                emit("GAME OVER - CORRECT ACCUSATION", {
                    "game_id": game_id,
                    "accuser": player_id,
                    "suspect": suspect,
                    "room_id": room_id,
                    "weapon": weapon,
                    "state": loaded_game.state.to_json()
                }, broadcast=True)
            else:
                emit("FALSE ACCUSATION", {
                    "game_id": game_id,
                    "accuser": player_id,
                    "suspect": suspect,
                    "room_id": room_id,
                    "weapon": weapon,
                    "state": loaded_game.state.to_json()
                }, broadcast=True)                    
        else:
            emit("Could not load game", {"game_id": game_id}, broadcast=True)



# Event to load a game by ID from the database
@socketio.on("get_game")
def get_game(data):
    with app.app_context():
        game_id = data.get("game_id")

        # Create a new Game instance and load the data from the database
        loaded_game = Game(player_ids=None, num_players=0, status="inactive")  # Temporary values
        loaded = loaded_game.load_from_db(game_id)
        if loaded:
            # Print the game's info
            print(f"Game loaded: ID= {loaded_game.id}, Players IDs= {loaded_game.player_ids}, Num Players= {loaded_game.num_players}, Status= {loaded_game.status}, State= {loaded_game.state}")

            # Emit the loaded game info to all connected clients
            emit("game_loaded", {
                "id": loaded_game.id,
                "player_ids": json.dumps(loaded_game.player_ids),
                "num_players": loaded_game.num_players,
                "status": loaded_game.status,
                "state": loaded_game.state.to_json() 
            }, broadcast=True)
        else:
            # Print the game's info
            print(f"Game with ID={game_id} could not be loaded")
            emit("game_loaded_error", {"id": game_id}, broadcast=True)

            # # Emit the loaded game info to all connected clients
            # emit("game_loaded", {
            #     "id": loaded_game.id,
            #     "num_players": loaded_game.num_players,
            #     "status": loaded_game.status,
            #     "state": loaded_game.state.to_json()
            # }, broadcast=True)

# TODO: ADD MORE MESSAGE HANDLERS FOR SPECIFIC ACTIONS

def load_from_db(game_id):
    loaded_game = Game(None, 0, "null")
    loaded = loaded_game.load_from_db(game_id)
    if loaded:
        return loaded_game
    else:
        return None


if __name__ == "__main__":
    socketio.run(app, debug=True)
