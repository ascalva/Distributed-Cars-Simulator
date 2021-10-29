from src import db

class User(db.Model) :
    client_id = db.Column(db.String, primary_key=True)
    # position  =
