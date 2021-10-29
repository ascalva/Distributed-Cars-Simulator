from flask import Blueprint, jsonify, request
from src   import app


actions = Blueprint("actions", __name__, url_prefix="/actions")


@actions.route("/login", methods=["GET", "POST"], strict_slashes=False)
def client_login() :
    client_id = request.form.get("id")
    client_ip = request.remote_addr

    # TODO: Create user (assign position?)

    return jsonify({
        "status"  : "ok",
        "message" : f"will create new account for {client_id} at {client_ip}"
    })


@actions.route("/getNeighbors", methods=["GET"], strict_slashes=False)
def getNeighbors() :
    return jsonify([])


@actions.route("/move", methods=["GET", "POST"], strict_slashes=False)
def move() :
    return jsonify({
        "front" : 0,
        "back"  : 0,
        "left"  : 0,
        "right" : 0
    })



