from src.server            import db, login
from flask_login           import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

import numpy as np

class User(UserMixin, db.Model) :
    id         = db.Column(db.String(128), primary_key=True)
    ip_address = db.Column(db.String(16), nullable=False)
    position_x = db.Column(db.Integer,    nullable=False)
    position_y = db.Column(db.Integer,    nullable=False)

    def __init__(self, client_id, ip_address, pos_x, pos_y) :
        self.id         = client_id
        self.ip_address = ip_address
        self.position_x = pos_x
        self.position_y = pos_y

    def setPosition(self, x, y) :
        self.position_x = x
        self.position_y = y

    def updateIP(self, ip_address) :
        self.ip_address = ip_address

    @hybrid_property
    def position(self) :
        return (self.position_x, self.position_y)

    @hybrid_property
    def position_(self) :
        return np.array([self.position_x, self.position_y])


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
