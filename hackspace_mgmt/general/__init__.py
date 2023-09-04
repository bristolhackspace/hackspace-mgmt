from flask import Blueprint, render_template
from . import enroll_card

bp = Blueprint("general", __name__)

@bp.route("/")
def index():
    return render_template("index.html")

def init_app(app):
    app.register_blueprint(bp)
    app.register_blueprint(enroll_card.bp, url_prefix="/enroll")