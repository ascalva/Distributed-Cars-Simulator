import numpy as np

from flask             import Blueprint, jsonify, render_template, request
from src.server        import app, db
from src.server.models import User, Obstacle
from .environment      import *


view = Blueprint("view", __name__, url_prefix="/")


@view.route("/",      methods=['GET'], strict_slashes=False)
@view.route("/index", methods=['GET'], strict_slashes=False)
def index() :
    # Test getting user address.
    print(f"User address: {request.remote_addr}")

    return render_template("home.html")

@view.route("/createObstacle/<x_pos>/<y_pos>", methods=["GET", "POST"], strict_slashes=False)
def createObstacle(x_pos, y_pos) :
    x_pos = int(x_pos)
    y_pos = int(y_pos)

    if is_empty(x_pos, y_pos) :
        o = Obstacle(x_pos, y_pos)
        db.session.add(o)
        db.session.commit()

        return f"Successfully created obstacle at position ({x_pos}, {y_pos})"
    return f"Creation failed, position ({x_pos}, {y_pos}) is already taken!"

@view.route("/skeletonView", methods=["GET"], strict_slashes=False)
def skeletonView() :
    users     = User.query.all()
    obstacles = Obstacle.query.all()

    board_height, board_width = app.config["BOARD_DIMS"]

    board = np.chararray((board_height+1, board_width+1), unicode=True).astype(str)
    board[:] = "+"

    for c in users :
        x,y = c.position
        board[y, x] = "🚙"

    for o in obstacles :
        x, y = o.position
        board[y, x] = "█"


    boardv = ["&nbsp;&nbsp;&nbsp;&nbsp;".join(row) for row in board]
    boardv = "<br>".join(boardv)

    return boardv

@view.route("userView", methods = ["GET"], strict_slashes=False)
def userView() :
    users = User.query.all()

    return jsonify({u.id : tuple(u.position) for u in users})
