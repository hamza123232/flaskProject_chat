from flask_socketio import SocketIO, emit
from flask import request, Flask, send_file
import json
import os
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
def handle_message(data,filename):
    name = request.sid
    server_name = data['server_name']
    message = data['message']
    print(server_name, ":", message)
    if message.lower() == "bye":
        socket_server.disconnect(request.sid)
        print("File uploaded:", filename)
        broadcast_message(name + " uploaded file: " + filename)
    else:
        broadcast_message(name + ": " + message)
@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist("attachment")
    for file in files:
        filename = file.filename
        file.save(filename)
    return "File uploaded successfully"
@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    try:
        return send_file(filename, as_attachment=True)
    except FileNotFoundError:
        return "File not found"

def broadcast_message(message):
    socket_server.emit('message', message, namespace='/', skip_sid=request.sid)


if __name__ == '__main__':
    socket_server.run(app, port=8080)
