from flask             import Blueprint, jsonify, request
from flask_login       import current_user, login_user, logout_user, login_required
from src.server        import app, db
from src.server.models import User, Obstacle
from .environment      import *


actions = Blueprint("actions", __name__, url_prefix="/actions")


@actions.route("/login", methods=["GET", "POST"], strict_slashes=False)
def client_login() :
    """
    Entrypoint for clients/cars, establishes "connection" with board
    simulator. If entry for client with same ID exists, recorded
    position is returned. If client has never been seen, a new position
    is randomly generated and returned. User object is created for client.

    :param client_id: ID supplied by client, should be a unique identifier.
    :return:          JSON object containing position of client.
    """
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
        # User might have new IP address since last signin.
        u.updateIP(client_ip)
        db.session.commit()

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
    """
    Used to get IDs and corresponding IP addresses of clients nearby (threshold
    can be updated in config file).

    :param id: Current client's ID.
    :return:   Dictionary containing IDs as keys, and IP addresses as values.
    """
    client_id = request.form.get("id")
    users     = User.query.filter(User.id != client_id).all()

    # TODO: Temporarily return all other users (broadcast).
    return jsonify({c.id : c.ip_address for c in users})


@actions.route("/move", methods=["POST"], strict_slashes=False)
def move() :
    """
    Takes new position supplied by user and validates that the move satisfies:
        - Within board bounds
        - Moves to free space
        - Moves a total of one unit in any direction (Need to allow for no movement)
    Sensor data returned:
        - If move successful, return data of new surroundings.
        - If move unsccessful, return updated data surroundings about original position.

    :param client_id:  Current client's ID
    :param position_x: New x-position
    :param position_y: New y-position
    :return:           Return bool value indicating success status of movement, along
                       with sensor information of spaces adjacent to new position.
    """
    client_id  = request.form.get("id")
    position_x = request.form.get("position_x")
    position_y = request.form.get("position_y")

    u            = User.query.filter(User.id == client_id).first()
    x_old, y_old = u.position

    # TODO: Add proper lock.
    # Make sure move is valid.
    if proper_move(x_old, y_old, position_x, position_y) :
        u.setPosition(position_x, position_y)
        db.session.commit()

    # Get latest position, old if move failed, new otherwise.
    pos = u.position

    # Return sensor data, regardless of success
    return jsonify({
        "data"     : get_sensor_data(*pos),
        "position" : pos
    })

