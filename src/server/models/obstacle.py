from sqlalchemy.ext.hybrid import hybrid_property
from src.server            import db

class Obstacle(db.Model) :
    id         = db.Column(db.Integer, primary_key=True)
    position_x = db.Column(db.Integer)
    position_y = db.Column(db.Integer)

    # TODO: Add object descriptor.

    def __init__(self, pos_x, pos_y) :
        self.position_x = pos_x
        self.position_y = pos_y

    def setPosition(self, x, y) :
        self.position_x = x
        self.position_y = y

    @hybrid_property
    def position(self) :
        return (self.position_x, self.position_y)

