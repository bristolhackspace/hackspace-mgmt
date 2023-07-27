import os
import logging

from flask import Flask

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

    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .models import db
    db.init_app(app)

    from .general import general
    general.init_app(app)

    from .admin import admin
    admin.init_app(app)

    from . import machine_api
    app.register_blueprint(machine_api.bp)



    return app