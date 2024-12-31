from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('chatsection.html')

@socketio.on('message')
def handle_message(data):
    print(f"Message: {data}")
    send(data, broadcast=True)  # Broadcast message to all connected clients

@socketio.on('connect')
def handle_connect():
    print("A user connected.")
     

@socketio.on('disconnect')
def handle_disconnect():
    print("A user disconnected.")

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5001)
