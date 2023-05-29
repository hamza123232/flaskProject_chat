from flask_socketio import SocketIO, emit
from flask import request, Flask
import json
app = Flask(__name__)
socket_server = SocketIO(app)

@socket_server.on('connect')
def handle_connect():
    name = request.sid
    print("handle connect")
    print("Connection from", request.remote_addr)
    print(name, "connected")

    broadcast_message(name + " has joined the chat.")
    message_data = {'server_name': 'your_server_name', 'message': name + " has joined.."}
    socket_server.emit('message', json.dumps(message_data),namespace='/')

@socket_server.on('disconnect')
def handle_disconnect():
    name = request.sid
    broadcast_message(name + " has left the chat.")

@socket_server.on('message')
def handle_message(data):
    name = request.sid
    server_name = data['server_name']
    message = data['message']
    print(server_name, ":", message)
    if message.lower() == "bye":
        socket_server.disconnect(request.sid)
    else:
        broadcast_message(name + ": " + message)

def broadcast_message(message):
    socket_server.emit('message', message, namespace='/', skip_sid=request.sid)


if __name__ == '__main__':
    socket_server.run(app, port=8080)
