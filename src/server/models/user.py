from src.server            import db, login
from flask_login           import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

class User(UserMixin, db.Model) :
    client_id  = db.Column(db.String(128), primary_key=True)
    ip_address = db.Column(db.String(16), nullable=False)
    position_x = db.Column(db.Integer)
    position_y = db.Column(db.Integer)

    def __init__(self, client_id, ip_address) :
        self.client_id  = client_id
        self.ip_address = ip_address

    def setPosition(self, x, y) :
        self.position_x = x
        self.position_y = y

    @hybrid_property
    def getPosition(self) :
        return (self.position_x, self.position_y)


@login.user_loader
def load_user(client_id):
    return User.query.get(client_id)
