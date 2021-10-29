from flask          import Flask
from flask_socketio import SocketIO
from src.config     import Config

app = Flask(__name__)
app.config.from_object(Config)

# socketio = SocketIO(app)


from src.routes import actions, view

app.register_blueprint(actions)
app.register_blueprint(view)

