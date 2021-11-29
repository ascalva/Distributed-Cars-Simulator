from flask                  import Blueprint, jsonify, request
from flask_login            import current_user
from src.server             import app, db
from src.server.models.user import User


actions = Blueprint("actions", __name__, url_prefix="/actions")


@actions.route("/login", methods=["GET", "POST"], strict_slashes=False)
def client_login() :
    client_id = request.form.get("id")
    client_ip = request.remote_addr

    # TODO: Create user (assign position?)
    if (u := User.query.filter(User.client_id == client_id).first()) is None :
        u = User(client_id, client_ip)

        db.session.add(u)
        db.session.commit()
        print("Created user")

        # TODO: Generate new position, validate nothing exists there.
        pos_x, pos_y = 0, 0
        message      = "Creating user"

    else:
        print("user exists")
        pos_x, pos_y = u.getPosition()
        message      = "User already exists."

    return jsonify({
        "status"     : "ok",
        "message"    : message,
        "position_x" : pos_x,
        "position_y" : pos_y
    })


@actions.route("/getNeighbors", methods=["GET"], strict_slashes=False)
def getNeighbors() :
    users = User.query.filter(User.client_id != current_user_client_id).all()

    # TODO: Temporarily return all other users (broadcast).
    return jsonify({c.client_id : c.client_ip for c in users})


@actions.route("/move", methods=["POST"], strict_slashes=False)
def move() :
    position_x = request.form.get("position_x")
    position_y = request.form.get("position_y")

    # TODO: Return sensor info.


