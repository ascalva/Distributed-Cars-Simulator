from flask          import Flask
# from flask_socketio import SocketIO
from src.server.config     import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate    import Migrate
from flask_login      import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

# socketio = SocketIO(app)

db      = SQLAlchemy(app)
migrate = Migrate(app, db)
db.init_app(app)

login   = LoginManager(app)

from src.server.routes import actions, view

# Create db.
db.create_all()
db.session.commit()

app.register_blueprint(actions)
app.register_blueprint(view)

