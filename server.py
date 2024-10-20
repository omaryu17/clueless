import eventlet
eventlet.monkey_patch()

from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# later replace * with actual client url once it"s deployed

socketio = SocketIO(app, cors_allowed_origins="*")

# map client id (random hash) to player id (>= 0)
clients = {}
# count = 0

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
    with app.app_context:
        print(f"Player {request.sid} performed an action")
        emit("server_broadcast", {"response": f"Player {request.sid} performed an action!"}, broadcast=True)

# TODO: ADD MORE MESSAGE HANDLERS FOR SPECIFIC ACTIONS


if __name__ == "__main__":
    socketio.run(app, debug=True)
