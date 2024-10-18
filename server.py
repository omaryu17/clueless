import eventlet
eventlet.monkey_patch()

from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# later replace * with actual client url once it's deployed

socketio = SocketIO(app, cors_allowed_origins="*")

# HTTP route for cron job to keep server alive
@app.route('/ping', methods=['GET'])
def ping():
    with app.app_context():
        return jsonify({"response": "pong active"})

# handle client connection
@socketio.on('connect')
def handle_connect():
    with app.app_context():
        print('Client connected')
        emit('server_message', {'response': 'Welcome to the game!'})
        print("emitted")

# handle client disconnection
@socketio.on('disconnect')
def handle_disconnect():
    with app.app_context():
        print('Client disconnected')

# handle message from client, then broadcast to all connected clients
@socketio.on('client_message')
def handle_client_message(data):
    message = data['message']
    print(f"Message from client: {message}")
    emit('server_message', {'response': f"Broadcast: {message}"}, broadcast=True)
    print("emitted")

# TODO: ADD MORE MESSAGE HANDLERS FOR SPECIFIC ACTIONS

if __name__ == "__main__":
    socketio.run(app, debug=True)
