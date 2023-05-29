import socketio
import time
import socket
import threading
import json

socket_client = socketio.Client()

@socket_client.event
def connect():
    print("Connected to the server")

@socket_client.event
def message(data):
    server_name = name  # Update the server_name variable with the name provided
    message = data
    print(server_name, ":", message)

def send_message():
    while True:
        message = input("enter message")
        if message.lower() == "bye":
            socket_client.disconnect()
            break
        else:
            socket_client.emit('message', {'server_name': name, 'message': message})

if __name__ == '__main__':
    name = input("Enter your name: ")
    server_name = input("Enter the server name: ")
    connected = False

    while not connected:
        try:
            server_ip = socket.gethostbyname(socket.gethostname())
            server_address = f"http://127.0.0.1:8080"
            socket_client.connect(server_address)
            print("Socket established")
            connected = True
        except Exception as ex:
            print("Failed to establish initial connection to server:", type(ex).__name__)
            time.sleep(2)

    socket_client.emit('connect')
    socket_client.emit('message', {'server_name': server_name, 'message': name + " has joined.."})

    message_thread = threading.Thread(target=send_message)
    message_thread.start()

    socket_client.wait()
