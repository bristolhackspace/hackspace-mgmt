import os

from flask import Flask, render_template
from . import database
from . import models

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="postgresql+psycopg2://postgres:postgres@localhost:5432/hackspace"
    )
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    database.init_db(app)

    from . import general
    app.register_blueprint(general.bp)

    from . import equipment
    app.register_blueprint(equipment.bp)

    from . import machine_api
    app.register_blueprint(machine_api.bp)

    @app.route("/")
    def home():
        return render_template("home.html")

    return app