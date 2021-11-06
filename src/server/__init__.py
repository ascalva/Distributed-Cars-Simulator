from flask          import Flask
from flask_socketio import SocketIO
from src.server.config     import Config

app = Flask(__name__)
app.config.from_object(Config)

# socketio = SocketIO(app)


from src.server.routes import actions, view

app.register_blueprint(actions)
app.register_blueprint(view)

