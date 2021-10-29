from flask import Blueprint, jsonify, render_template
from src   import app


view = Blueprint("view", __name__, url_prefix="/")


@view.route("/",      methods=['GET'], strict_slashes=False)
@view.route("/index", methods=['GET'], strict_slashes=False)
def index() :
    return render_template("home.html")

