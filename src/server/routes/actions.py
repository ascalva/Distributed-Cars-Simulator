from flask             import Blueprint, jsonify, request
from flask_login       import current_user, login_user, logout_user, login_required
from src.server        import app, db
from src.server.models import User, Obstacle
from .environment      import get_empty_space


actions = Blueprint("actions", __name__, url_prefix="/actions")


@actions.route("/login", methods=["GET", "POST"], strict_slashes=False)
def client_login() :
    client_id = request.form.get("id")
    client_ip = request.remote_addr

    # Check if user exists, if not create and assign position.
    if (u := User.query.filter(User.id == client_id).first()) is None :
        pos = get_empty_space()
        u   = User(client_id, client_ip, *pos)

        db.session.add(u)
        db.session.commit()

        message = "Created user."

    else:
        pos     = u.position
        message = "User already exists."

    # Login user.
    login_user(u)

    return jsonify({
        "status"     : "ok",
        "message"    : message,
        "position"   : list(pos)
    })


@actions.route("/getNeighbors", methods=["GET", "POST"], strict_slashes=False)
def getNeighbors() :
    client_id = request.form.get("id")
    users     = User.query.filter(User.id != client_id).all()

    # # TODO: Temporarily return all other users (broadcast).
    return jsonify({c.id : c.ip_address for c in users})


@actions.route("/move", methods=["POST"], strict_slashes=False)
def move() :
    client_id  = request.form.get("id")
    position_x = request.form.get("position_x")
    position_y = request.form.get("position_y")

    # TODO: Return sensor info.


