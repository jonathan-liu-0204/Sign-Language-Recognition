from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from datetime import datetime

async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['TEMPLATES_AUTO_RELOAD'] = True
socketio = SocketIO(app)


@socketio.on("image")
def process(msg):
    print(msg)
    # do image processing thing
    emit("answer", 'Server received message "%s" at %s' % (msg, datetime.now().strftime("%H:%M:%S")))


@app.route("/")
def home():
    return render_template('website.html', async_mode=socketio.async_mode)


if __name__ == "__main__":
    socketio.run(app, debug=True, port=5002)
