from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app)
@app.route("/")
def health_checket():
    return "working"

if __name__ == '__main__':
    socketio.run(app, debug=True,port=8080)
