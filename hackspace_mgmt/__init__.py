import os

from flask import Flask, render_template
from flask_admin import Admin

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
    )
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import general
    app.register_blueprint(general.bp)

    from . import equipment
    app.register_blueprint(equipment.bp)

    from . import api
    app.register_blueprint(api.bp)

    @app.route("/")
    def home():
        return render_template("home.html")

    return app