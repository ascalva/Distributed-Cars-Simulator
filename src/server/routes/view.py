from flask      import Blueprint, jsonify, render_template, request
from src.server import app


view = Blueprint("view", __name__, url_prefix="/")


@view.route("/",      methods=['GET'], strict_slashes=False)
@view.route("/index", methods=['GET'], strict_slashes=False)
def index() :
    # Test getting user address.
    print(f"User address: {request.remote_addr}")

    return render_template("home.html")

