from flask import Blueprint, jsonify
from src   import app


actions = Blueprint("actions", __name__, url_prefix="/actions")


@actions.route("/actions/login", methods=["GET", "POST"], strict_slashes=False)
def client_login() :
    return ""


@actions.route("/actions/getNeighbors", methods=["GET"], strict_slashes=False)
def getNeighbors() :
    return jsonify([])


@actions.route("/actions/move", methods=["GET", "POST"], strict_slashes=False)
def move() :
    return jsonify({
        "front" : 0,
        "back"  : 0,
        "left"  : 0,
        "right" : 0
    })



