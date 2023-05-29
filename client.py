import os
import sys
import socketio
import time
import socket
import threading
import requests
import json
from tkinter import Tk, filedialog

socket_client = socketio.Client()

@socket_client.event
def connect():
    print("Connected to the server")

@socket_client.event
def message(data):
    server_name = name  # Update the server_name variable with the name provided
    message = data
    print(server_name, ":", message)
server_url = f"http://127.0.0.1:8080"
def select_file():
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if os.path.isfile(file_path):
            return file_path
        else:
            print("Invalid file path.")
    else:
        print("No file path provided.")

    return None
def upload(file_path):
    url = f"{server_url}/upload"
    files = {'attachment': open(file_path, 'rb')}
    response = requests.post(url, files=files)
    if response.status_code == 200:
        print("File uploaded successfully")
    else:
        print("File upload failed")
def download(filename):
    url = f"{server_url}/download/{filename}"
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        print("File downloaded successfully")
    else:
        print("File download failed")
def send_message():
    while True:
        message = input("enter message")
        if message.lower() == "bye":
            socket_client.disconnect()
            break

        elif message.lower()=='upload':
            selected_file = select_file()
            if selected_file:
                upload(selected_file)
        elif message.lower()=='download':
            response = requests.get(f"{server_url}/listfiles")
            if response.status_code == 200:
                available_files = response.json()
                if available_files:
                    print("Available files:")
                    for file in available_files:
                        print(file)
                    selected_file = input("Enter the filename to download: ")
                    if selected_file in available_files:
                        download(selected_file)
                    else:
                        print("Invalid filename.")
                else:
                    print("No files available for download.")
            else:
                print("Failed to retrieve the list of available files.")
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
